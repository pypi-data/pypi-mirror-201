from typing import Optional

import ai.h2o.featurestore.api.v1.CoreService_pb2 as pb
from ai.h2o.featurestore.api.v1.CoreService_pb2_grpc import CoreServiceStub

from ..entities.feature_view import FeatureView


class FeatureViews:
    def __init__(self, stub: CoreServiceStub, project):
        self._project = project
        self._stub = stub

    def create(self, name: str, query, description: str = ""):
        request = pb.CreateFeatureViewRequest(
            name=name,
            description=description,
            project_id=self._project.id,
            query=query._to_proto(),
        )
        response = self._stub.CreateFeatureView(request)
        return FeatureView(self._stub, response.feature_view)

    def get(self, name: str, version: Optional[int] = None):
        request = pb.GetFeatureViewRequest(project_id=self._project.id, name=name, version=(version or 0))
        resource = self._stub.GetFeatureView(request)
        return FeatureView(self._stub, resource.feature_view)

    def list(self):
        request = pb.ListFeatureViewsRequest(project_id=self._project.id)
        response = self._stub.ListFeatureViews(request)
        return [FeatureView(self._stub, feature_view) for feature_view in response.feature_views]
