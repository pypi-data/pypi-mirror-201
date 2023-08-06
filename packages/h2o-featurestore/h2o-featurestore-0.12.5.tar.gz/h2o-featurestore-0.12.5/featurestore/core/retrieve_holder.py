import time
from concurrent.futures import ThreadPoolExecutor

from ai.h2o.featurestore.api.v1 import CoreService_pb2 as pb

from .commons.spark_utils import SparkUtils
from .job_info import JobInfo
from .utils import Utils


class RetrieveAsLinksCommon:
    def _get_job(self, job_id):
        return self._stub.GetJob(job_id)

    def _get_retrieve_links_output(self, job_id):
        return self._stub.GetRetrieveAsLinksJobOutput(job_id)

    def download(self, output_dir=None):
        self._process_lazy_ingest_task()
        if not self._job_id:
            self._job_id = self._start_retrieve_links_job()

        info = JobInfo(self._stub, self._job_id)
        while not self._get_job(self._job_id).done:
            info.show_progress()
            time.sleep(2)
        info.show_progress()  # there is possibility that some progress was pushed before finishing job
        retrieve_as_links_response = self._get_retrieve_links_output(self._job_id)
        return Utils.download_files(output_dir, retrieve_as_links_response.download_links)

    def download_async(self, output_dir=None):
        future = self._thread_pool.submit(self.download, output_dir)
        return DownloadFuture(future)

    def _start_retrieve_links_job(self):
        request = self._create_retrieve_request()
        return self._stub.StartRetrieveAsLinksJob(request)

    def _create_retrieve_request(self, spark_session=None):
        session_id = ""
        if spark_session is not None:
            session_id = spark_session.conf.get("ai.h2o.featurestore.sessionId", "")
        request = pb.RetrieveRequest()
        request.feature_set.CopyFrom(self._feature_set)
        request.session_id = session_id
        if self._start_date_time is not None:
            request.start_date_time = self._start_date_time
        if self._end_date_time is not None:
            request.end_date_time = self._end_date_time
        request.ingest_id = self._ingest_id
        return request

    def _process_lazy_ingest_task(self):
        request = pb.LazyIngestRequest(
            feature_set_id=self._feature_set.id, feature_set_version=self._feature_set.version
        )
        response = self._stub.StartLazyIngestTask(request)
        if response.job_id.job_id:
            print(
                "No previous ingestion found. Lazy ingest task will start. "
                "New minor version will be created and retrieved from."
            )
            info = JobInfo(self._stub, response.job_id)
            while not self._get_job(response.job_id).done:
                info.show_progress()
                time.sleep(2)
            info.show_progress()  # there is possibility that some progress was pushed before finishing job
            feature_set_response = self._stub.GetIngestJobOutput(response.job_id).feature_set
            self._feature_set.version = feature_set_response.version


class RetrieveHolder(RetrieveAsLinksCommon):
    def __init__(self, stub, feature_set, start_date_time, end_date_time, ingest_id):
        self._stub = stub
        self._thread_pool = ThreadPoolExecutor(5)
        self._feature_set = feature_set
        self._start_date_time = start_date_time
        self._end_date_time = end_date_time
        self._retrieve_as_spark_response = None
        self._job_id = None
        self._ingest_id = ingest_id

    def download(self, output_dir=None):
        return super(RetrieveHolder, self).download(output_dir)

    def download_async(self, output_dir=None):
        return super(RetrieveHolder, self).download_async(output_dir)

    def as_spark_frame(self, spark_session):
        from pyspark.sql.functions import col, from_utc_timestamp, lit, to_timestamp, unix_timestamp

        self._process_lazy_ingest_task()
        if self._retrieve_as_spark_response is None:
            request = self._create_retrieve_request(spark_session)
            self._retrieve_as_spark_response = self._stub.RetrieveAsSpark(request)
        resp = self._retrieve_as_spark_response
        spark_session.conf.set("ai.h2o.featurestore.sessionId", resp.session_id)
        SparkUtils.configure_user_spark(spark_session)
        for k, v in resp.options.items():
            spark_session.conf.set(k, v)
        if self._retrieve_as_spark_response.delta_version == -1:
            df = spark_session.read.format("delta").load(resp.cache_path)
        else:
            df = (
                spark_session.read.format("delta")
                .option("versionAsOf", self._retrieve_as_spark_response.delta_version)
                .load(resp.cache_path)
            )
        retrieve_scope = resp.retrieve_scope
        start_timestamp = retrieve_scope.start_date_time.seconds
        end_timestamp = retrieve_scope.end_date_time.seconds
        timestamp_col = "timestamp_" + str(round(time.time() * 1000))
        if self._ingest_id:
            output_df = df.filter(col("ingest_id") == lit(self._ingest_id))
        elif self._feature_set.time_travel_column:
            output_df = (
                df.withColumn(
                    timestamp_col,
                    unix_timestamp(
                        from_utc_timestamp(
                            to_timestamp(
                                col("`" + self._feature_set.time_travel_column + "`"),
                                self._feature_set.time_travel_column_format,
                            ),
                            spark_session.conf.get("spark.sql.session.timeZone"),
                        )
                    ),
                )
                .filter(col(timestamp_col) <= end_timestamp)
                .filter(col(timestamp_col) >= start_timestamp)
            ).drop(timestamp_col)
        else:
            output_df = df.filter(col("time_travel_column_auto_generated") <= end_timestamp).filter(
                col("time_travel_column_auto_generated") >= start_timestamp
            )
        internal_columns = ["ingest_id"] + [column for column in df.columns if column.startswith("__")]
        return output_df.drop(*internal_columns)


class DownloadFuture:
    def __init__(self, future):
        self._future = future
        self._result = None

    def is_done(self) -> bool:
        return self._future.done()

    def get_result(self):
        if not self._result:
            if not self.is_done():
                raise Exception("Job has not finished yet!")
            self._result = self._future.result()
        return self._result
