import datetime
from typing import Optional, Tuple

import ai.h2o.featurestore.api.v1.CoreService_pb2 as pb
from ai.h2o.featurestore.api.v1.CoreService_pb2_grpc import CoreServiceStub

from .. import interactive_console
from ..entities.create_ml_dataset_job import CreateMLDatasetJob
from ..entities.ml_dataset import MLDataset
from ..utils import Utils


class MLDatasets:
    def __init__(self, stub: CoreServiceStub, feature_view):
        self._feature_view = feature_view
        self._stub = stub

    @interactive_console.record_stats
    def create(
        self,
        name: str,
        description: str = "",
        start_date_time: Optional[datetime.datetime] = None,
        end_date_time: Optional[datetime.datetime] = None,
    ):
        job, ml_dataset = self.create_async(name, description, start_date_time, end_date_time)
        return job.wait_for_result()

    def create_async(
        self,
        name: str,
        description: str = "",
        start_date_time: Optional[datetime.datetime] = None,
        end_date_time: Optional[datetime.datetime] = None,
    ) -> Tuple[CreateMLDatasetJob, MLDataset]:
        request = pb.CreateMLDatasetRequest(
            name=name,
            description=description,
            feature_view_id=self._feature_view.id,
            feature_view_version=self._feature_view.version,
            start_date_time=Utils.date_time_to_proto_timestamp(start_date_time),
            end_date_time=Utils.date_time_to_proto_timestamp(end_date_time),
        )

        response = self._stub.CreateMLDataset(request)
        return CreateMLDatasetJob(self._stub, response.job), MLDataset(self._stub, response.ml_dataset)

    def get(self, name: str):
        request = pb.GetMLDatasetRequest(
            feature_view_id=self._feature_view.id,
            feature_view_version=self._feature_view.version,
            ml_dataset_name=name,
        )

        ml_dataset = self._stub.GetMLDataset(request)
        return MLDataset(self._stub, ml_dataset)

    def list(self):
        request = pb.ListMLDatasetsRequest(
            feature_view_id=self._feature_view.id,
            feature_view_version=self._feature_view.version,
        )

        response = self._stub.ListMLDatasets(request)
        return [MLDataset(self._stub, ml_dataset) for ml_dataset in response.ml_datasets]
