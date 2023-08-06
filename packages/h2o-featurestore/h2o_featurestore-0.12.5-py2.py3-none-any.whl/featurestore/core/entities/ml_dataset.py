import datetime
import json

from google.protobuf.timestamp_pb2 import Timestamp

import ai.h2o.featurestore.api.v1.CoreService_pb2 as pb
from ai.h2o.featurestore.api.v1.CoreService_pb2_grpc import CoreServiceStub

from ..utils import Utils
from .ml_data_feature import MLDatasetFeature


class MLDataset:
    def __init__(self, stub: CoreServiceStub, ml_dataset_proto):
        ml_dataset = pb.MLDataset()
        ml_dataset.CopyFrom(ml_dataset_proto)
        self._ml_dataset = ml_dataset
        self._stub = stub

    @property
    def id(self):
        return self._ml_dataset.id

    @property
    def name(self):
        return self._ml_dataset.name

    @property
    def description(self):
        return self._ml_dataset.description

    @property
    def primary_keys(self):
        return self._ml_dataset.primary_keys

    @description.setter
    def description(self, value):
        update_request = pb.UpdateMLDatasetRequest(
            ml_dataset_id=self.id,
            description=value,
        )
        ml_dataset_proto = self._stub.UpdateMLDataset(update_request)
        ml_dataset = pb.MLDataset()
        ml_dataset.CopyFrom(ml_dataset_proto)
        self._ml_dataset = ml_dataset

    @property
    def start_date_time(self):
        timestamp: Timestamp = self._ml_dataset.start_date_time
        if timestamp:
            return datetime.datetime.fromtimestamp(timestamp.ToMilliseconds() / 1000, tz=datetime.timezone.utc)
        else:
            return None

    @property
    def end_date_time(self):
        timestamp: Timestamp = self._ml_dataset.end_date_time
        if timestamp:
            return datetime.datetime.fromtimestamp(timestamp.ToMilliseconds() / 1000, tz=datetime.timezone.utc)
        else:
            return None

    @property
    def features(self):
        return [MLDatasetFeature(feature) for feature in self._ml_dataset.features]

    def delete(self):
        request = pb.DeleteMLDatasetRequest(ml_dataset_id=self.id)
        self._stub.DeleteMLDataset(request)

    def download(self, output_dir=None):
        request = pb.RetrieveMLDatasetAsAsLinksRequest(ml_dataset_id=self.id)
        response = self._stub.RetrieveMLDatasetAsLinks(request)

        return Utils.download_files(output_dir, response.download_links)

    def as_spark_frame(self, spark_session):
        from ..commons.spark_utils import SparkUtils

        session_id = spark_session.conf.get("ai.h2o.featurestore.sessionId", "")
        request = pb.RetrieveMLDatasetAsSparkRequest(ml_dataset_id=self.id, session_id=session_id)

        response = self._stub.RetrieveMLDatasetAsSpark(request)
        spark_session.conf.set("ai.h2o.featurestore.sessionId", response.session_id)

        SparkUtils.configure_user_spark(spark_session)
        for k, v in response.options.items():
            spark_session.conf.set(k, v)

        return spark_session.read.format("parquet").load(response.path)

    def retrieve_online(self, *keys):
        request = pb.RetrieveMLDatasetOnlineRequest(ml_dataset_id=self.id, keys=[str(key) for key in keys])
        json_row = self._stub.RetrieveMLDatasetOnline(request).row
        return json.loads(json_row)

    def __repr__(self):
        return Utils.pretty_print_proto(self._ml_dataset)

    def __str__(self):
        nl = "\n"
        return (
            f"Name                  : {self.name} \n"
            f"Description           : {self.description} \n"
            f"Feature view version  : {self._ml_dataset.feature_view_version} \n"
            f"State                 : {self._ml_dataset.state} \n"
            f"Primary keys          : {self.primary_keys} \n"
            f"Features              : \n{nl.join(self._custom_feature_fields())} \n"
        )

    def _custom_feature_fields(self):
        tmp_list = list()
        for feature in self.features:
            s = (
                "   {\n"
                f"     Name             : {feature.name} \n"
                f"     Data type        : {feature.data_type} \n"
                f"     Is primary key?  : {feature.is_primary_key} \n"
                "   }"
            )
            tmp_list.append(s)
        return tmp_list
