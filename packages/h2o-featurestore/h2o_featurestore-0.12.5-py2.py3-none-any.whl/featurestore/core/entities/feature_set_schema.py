import ai.h2o.featurestore.api.v1.CoreService_pb2 as pb
import ai.h2o.featurestore.api.v1.FeatureSetProtoApi_pb2 as FeatureSetApi

from ..schema import FeatureSchema, FeatureSchemaSpecialData, Schema


class FeatureSetSchema:
    def __init__(self, stub, feature_set):
        self._feature_set = feature_set
        self._stub = stub

    def get(self):
        return Schema.create_from(self._feature_set)

    def is_compatible_with(self, new_schema, compare_data_types=True):
        request = pb.FeatureSetSchemaCompatibilityRequest()
        request.original_schema.extend(self.get()._to_proto_schema())
        request.new_schema.extend(new_schema._to_proto_schema())
        request.compare_data_types = compare_data_types
        response = self._stub.IsFeatureSetSchemaCompatible(request)
        return response.is_compatible

    def patch_from(self, new_schema, compare_data_types=True):
        request = pb.FeatureSetSchemaPatchRequest()
        request.original_schema.extend(self.get()._to_proto_schema())
        request.new_schema.extend(new_schema._to_proto_schema())
        request.compare_data_types = compare_data_types
        response = self._stub.FeatureSetSchemaPatch(request)
        return Schema(self._create_schema_from_proto(response.schema), True)

    @staticmethod
    def _create_schema_from_proto(schema):
        return [
            FeatureSchema(
                feature_schema.name,
                feature_schema.data_type,
                nested_features_schema=FeatureSetSchema._create_schema_from_proto(feature_schema.nested),
                special_data=FeatureSchemaSpecialData(
                    spi=feature_schema.special_data.spi,
                    pci=feature_schema.special_data.pci,
                    rpi=feature_schema.special_data.rpi,
                    demographic=feature_schema.special_data.demographic,
                    sensitive=feature_schema.special_data.sensitive,
                ),
                _feature_type=FeatureSetApi.FeatureType.Name(feature_schema.feature_type),
                description=feature_schema.description,
                classifiers=set(feature_schema.classifiers),
            )
            for feature_schema in schema
        ]
