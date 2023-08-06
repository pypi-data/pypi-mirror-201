import datetime
import json
import time
from typing import Optional

import ai.h2o.featurestore.api.v1.CoreService_pb2 as pb
import ai.h2o.featurestore.api.v1.FeatureSetProtoApi_pb2 as FeatureSetApi
import ai.h2o.featurestore.api.v1.OnlineApi_pb2 as OnlineApi
import ai.h2o.featurestore.api.v1.TimeToLiveApi_pb2 as TimeToLiveApi

from .. import interactive_console
from ..access_type import AccessType
from ..collections.ingest_history import IngestHistory
from ..collections.scheduled_tasks import ScheduledTasks
from ..commons.case_insensitive_dict import CaseInsensitiveDict
from ..credentials import CredentialsHelper
from ..data_source_wrappers import SparkDataFrame
from ..entities.backfill_option import BackfillOption
from ..entities.feature import Feature
from ..job_info import JobInfo
from ..retrieve_holder import RetrieveHolder
from ..utils import Utils
from .feature_set_ref import FeatureSetRef
from .feature_set_schema import FeatureSetSchema
from .ingest_job import IngestJob
from .materialization_online_job import MaterializationOnlineJob
from .recommendation import Recommendation
from .user import User


class FeatureSet:
    def __init__(self, stub, feature_set):
        fs = pb.FeatureSet()
        fs.CopyFrom(feature_set)
        self._feature_set = fs
        self._stub = stub

    @property
    def id(self):
        return self._feature_set.id

    @property
    def project(self):
        return self._feature_set.project

    @property
    def feature_set_name(self):
        return self._feature_set.feature_set_name

    @property
    def version(self) -> str:
        return self._feature_set.version

    @property
    def major_version(self) -> int:
        return int(self.version.split(".")[0])

    @property
    def version_change(self):
        return self._feature_set.version_change

    @property
    def time_travel_column(self):
        return self._feature_set.time_travel_column

    @property
    def partition_by(self):
        return self._feature_set.partition_by

    @property
    def time_travel_column_format(self):
        return self._feature_set.time_travel_column_format

    @property
    def feature_set_type(self):
        return FeatureSetApi.FeatureSetType.Name(self._feature_set.feature_set_type)

    @feature_set_type.setter
    def feature_set_type(self, value):
        valid_values = FeatureSetApi.FeatureSetType.keys()
        if value.upper() in valid_values:
            update_request = pb.UpdateFeatureSetRequest(
                feature_set_id=self._feature_set.id,
                feature_set_version=self._feature_set.version,
                type=FeatureSetApi.FeatureSetType.Value(value.upper()),
                fields_to_update=[pb.FEATURE_SET_TYPE],
            )
            self._feature_set = self._stub.UpdateFeatureSet(update_request).updated_feature_set
        else:
            raise Exception("Invalid feature set type. Supported values are: " + ", ".join(map(str, valid_values)))

    @property
    def description(self):
        return self._feature_set.description

    @description.setter
    def description(self, value):
        update_request = pb.UpdateFeatureSetRequest(
            feature_set_id=self._feature_set.id,
            feature_set_version=self._feature_set.version,
            description=value,
            fields_to_update=[pb.FEATURE_SET_DESCRIPTION],
        )
        self._feature_set = self._stub.UpdateFeatureSet(update_request).updated_feature_set

    @property
    def owner(self):
        print('Owner field will be removed in 0.14.0. Please use "owners" instead.')
        return User(self._feature_set.owner)

    @owner.setter
    def owner(self, email):
        print('Owner field will be removed in 0.14.0. Please use "owners" instead.')
        request = pb.GetUserByMailRequest()
        request.email = email
        response = self._stub.GetUserByMail(request)
        user = response.user
        update_request = pb.FeatureSetUserFieldUpdateRequest()
        update_request.new_value.CopyFrom(user)
        header = FeatureSetApi.FeatureSetHeader(
            project_id=self._feature_set.project_id,
            feature_set_id=self._feature_set.id,
            feature_set_version=self._feature_set.version,
        )
        update_request.header.CopyFrom(header)
        self._stub.UpdateFeatureSetOwner(update_request)
        self.refresh()

    @property
    def author(self):
        return User(self._feature_set.author)

    @property
    def created_date_time(self):
        return Utils.timestamp_to_string(self._feature_set.created_date_time)

    @property
    def last_update_date_time(self):
        return Utils.timestamp_to_string(self._feature_set.last_update_date_time)

    @property
    def application_name(self):
        return self._feature_set.application_name

    @application_name.setter
    def application_name(self, value):
        update_request = pb.UpdateFeatureSetRequest(
            feature_set_id=self._feature_set.id,
            feature_set_version=self._feature_set.version,
            application_name=value,
            fields_to_update=[pb.FEATURE_SET_APPLICATION_NAME],
        )
        self._feature_set = self._stub.UpdateFeatureSet(update_request).updated_feature_set

    @property
    def deprecated(self):
        return self._feature_set.deprecated

    @deprecated.setter
    def deprecated(self, value):
        update_request = pb.UpdateFeatureSetRequest(
            feature_set_id=self._feature_set.id,
            feature_set_version=self._feature_set.version,
            deprecated=value,
            fields_to_update=[pb.FEATURE_SET_DEPRECATED],
        )
        self._feature_set = self._stub.UpdateFeatureSet(update_request).updated_feature_set

    @property
    def deprecated_date(self):
        return Utils.timestamp_to_string(self._feature_set.deprecated_date)

    @property
    def data_source_domains(self):
        return self._feature_set.data_source_domains

    @data_source_domains.setter
    def data_source_domains(self, value):
        if not isinstance(value, list):
            raise ValueError("data_source_domains accepts only list of strings as a value")

        update_request = pb.UpdateFeatureSetRequest(
            feature_set_id=self._feature_set.id,
            feature_set_version=self._feature_set.version,
            fields_to_update=[pb.FEATURE_SET_DATA_SOURCE_DOMAINS],
        )
        update_request.data_source_domains.extend(value)
        self._feature_set = self._stub.UpdateFeatureSet(update_request).updated_feature_set

    @property
    def tags(self):
        return self._feature_set.tags

    @tags.setter
    def tags(self, value):
        if not isinstance(value, list):
            raise ValueError("tags accepts only list of strings as a value")

        update_request = pb.UpdateFeatureSetRequest(
            feature_set_id=self._feature_set.id,
            feature_set_version=self._feature_set.version,
            fields_to_update=[pb.FEATURE_SET_TAGS],
        )
        update_request.tags.extend(value)
        self._feature_set = self._stub.UpdateFeatureSet(update_request).updated_feature_set

    @property
    def process_interval(self):
        return self._feature_set.process_interval

    @process_interval.setter
    def process_interval(self, value):
        update_request = pb.UpdateFeatureSetRequest(
            feature_set_id=self._feature_set.id,
            feature_set_version=self._feature_set.version,
            process_interval=value,
            fields_to_update=[pb.FEATURE_SET_PROCESS_INTERVAL],
        )
        self._feature_set = self._stub.UpdateFeatureSet(update_request).updated_feature_set

    @property
    def process_interval_unit(self):
        return pb.ProcessIntervalUnit.Name(self._feature_set.process_interval_unit)

    @process_interval_unit.setter
    def process_interval_unit(self, value):
        valid_units = pb.ProcessIntervalUnit.keys()
        if value.upper() in valid_units:
            update_request = pb.UpdateFeatureSetRequest(
                feature_set_id=self._feature_set.id,
                feature_set_version=self._feature_set.version,
                process_interval_unit=pb.ProcessIntervalUnit.Value(value.upper()),
                fields_to_update=[pb.FEATURE_SET_PROCESS_INTERVAL_UNIT],
            )
            self._feature_set = self._stub.UpdateFeatureSet(update_request).updated_feature_set
        else:
            raise Exception("Invalid process interval unit. Supported values are: " + ", ".join(map(str, valid_units)))

    @property
    def flow(self):
        return self._feature_set.flow

    @flow.setter
    def flow(self, value):
        update_request = pb.UpdateFeatureSetRequest(
            feature_set_id=self._feature_set.id,
            feature_set_version=self._feature_set.version,
            flow=value,
            fields_to_update=[pb.FEATURE_SET_FLOW],
        )
        self._feature_set = self._stub.UpdateFeatureSet(update_request).updated_feature_set

    @property
    def features(self):
        return CaseInsensitiveDict(
            {feature.name: Feature(self._stub, self, feature, feature.name) for feature in self._feature_set.features}
        )

    @property
    def primary_key(self):
        return self._feature_set.primary_key

    @primary_key.setter
    def primary_key(self, value):
        print(
            "Primary key setter will be removed in 0.14.0. Please use "
            + "createNewVersion with primaryKey argument instead."
        )
        update_request = pb.FeatureSetStringArrayFieldUpdateRequest()
        if isinstance(value, str):
            update_request.new_value.append(value)
        else:
            update_request.new_value.extend(value)
        header = FeatureSetApi.FeatureSetHeader(
            project_id=self._feature_set.project_id,
            feature_set_id=self._feature_set.id,
            feature_set_version=self._feature_set.version,
        )
        update_request.header.CopyFrom(header)
        self._stub.UpdateFeatureSetPrimaryKey(update_request)
        self.refresh()

    @property
    def statistics(self):
        return Statistics(self._feature_set)

    @property
    def time_to_live(self):
        return TimeToLive(self._stub, self)

    @property
    def special_data(self):
        return FeatureSetSpecialData(self._stub, self)

    @property
    def time_travel_scope(self):
        return FeatureSetScope(self._feature_set)

    @property
    def application_id(self):
        return self._feature_set.application_id

    @application_id.setter
    def application_id(self, value):
        update_request = pb.UpdateFeatureSetRequest(
            feature_set_id=self._feature_set.id,
            feature_set_version=self._feature_set.version,
            application_id=value,
            fields_to_update=[pb.FEATURE_SET_APPLICATION_ID],
        )
        self._feature_set = self._stub.UpdateFeatureSet(update_request).updated_feature_set

    @property
    def feature_set_state(self):
        return self._feature_set.feature_set_state

    @feature_set_state.setter
    def feature_set_state(self, value):
        update_request = pb.UpdateFeatureSetRequest(
            feature_set_id=self._feature_set.id,
            feature_set_version=self._feature_set.version,
            state=value,
            fields_to_update=[pb.FEATURE_SET_STATE],
        )
        self._feature_set = self._stub.UpdateFeatureSet(update_request).updated_feature_set

    @property
    def online(self):
        return Online(self._feature_set)

    @property
    def secret(self):
        return self._feature_set.secret

    @secret.setter
    def secret(self, value):
        update_request = pb.UpdateFeatureSetRequest(
            feature_set_id=self._feature_set.id,
            feature_set_version=self._feature_set.version,
            secret=value,
            fields_to_update=[pb.FEATURE_SET_SECRET],
        )
        self._feature_set = self._stub.UpdateFeatureSet(update_request).updated_feature_set

    @property
    def custom_data(self):
        return self._feature_set.custom_data

    @property
    def feature_classifiers(self):
        return self._feature_set.feature_classifiers

    def is_derived(self):
        return self._feature_set.derived_from.HasField("transformation")

    def _reference(self) -> FeatureSetRef:
        return FeatureSetRef(self.id, self.major_version)

    @custom_data.setter
    def custom_data(self, value):
        update_request = pb.UpdateFeatureSetRequest(
            feature_set_id=self._feature_set.id,
            feature_set_version=self._feature_set.version,
            custom_data=value,
            fields_to_update=[pb.FEATURE_SET_CUSTOM_DATA],
        )
        self._feature_set = self._stub.UpdateFeatureSet(update_request).updated_feature_set

    def create_new_version(
        self,
        schema=None,
        affected_features=None,
        reason="",
        primary_key=None,
        backfill_options: Optional[BackfillOption] = None,
    ):
        if schema is None and affected_features is None and primary_key is None:
            raise ValueError(
                "At least one of schema, affected_features or primary_key must be defined. "
                + "All values are supported as well"
            )
        request = pb.CreateNewFeatureSetVersionRequest()
        request.feature_set.CopyFrom(self._feature_set)
        request.reason = reason
        if schema:
            request.schema.extend(schema._to_proto_schema())
            if schema.is_derived():
                request.derived_from.CopyFrom(schema.derivation._to_proto())
        else:
            request.schema.extend(self.schema.get()._to_proto_schema())
        if affected_features:
            request.affected_features.extend(affected_features)
        if primary_key:
            request.primary_key.extend(primary_key)
        else:
            request.use_primary_key_from_previous_version = True
        if backfill_options:
            request.backfill_options.CopyFrom(backfill_options._to_proto(self._stub))
        response = self._stub.CreateNewFeatureSetVersion(request)
        if backfill_options:
            print(f"Backfill started with job id: '{response.job.job_id}'. Please use this job id to track progress.")
        return FeatureSet(self._stub, response.feature_set)

    def refresh(self):
        header = FeatureSetApi.FeatureSetHeader(
            project_id=self._feature_set.project_id,
            feature_set_id=self._feature_set.id,
            feature_set_version=self._feature_set.version,
        )
        request = pb.GetFeatureSetsLastMinorForCurrentMajorRequest()
        request.header.CopyFrom(header)
        self._feature_set = self._stub.GetFeatureSetsLastMinorForCurrentMajor(request).feature_set
        return self

    def delete(self, wait_for_completion=False):
        request = pb.DeleteFeatureSetRequest()
        request.feature_set.CopyFrom(self._feature_set)
        self._stub.DeleteFeatureSet(request)
        exists_request = pb.FeatureSetExistsRequest()
        exists_request.project_id = self._feature_set.project_id
        exists_request.feature_set_id = self._feature_set.id
        if wait_for_completion:
            while self._stub.FeatureSetExists(exists_request).exists:
                time.sleep(1)
                print("Waiting for feature set '{}' deletion".format(self._feature_set.feature_set_name))

    def add_owners(self, user_emails):
        return self._add_permissions(user_emails, pb.PermissionType.Owner)

    def add_editors(self, user_emails):
        return self._add_permissions(user_emails, pb.PermissionType.Editor)

    def add_consumers(self, user_emails):
        return self._add_permissions(user_emails, pb.PermissionType.Consumer)

    def add_sensitive_consumers(self, user_emails):
        return self._add_permissions(user_emails, pb.PermissionType.SensitiveConsumer)

    def add_viewers(self, user_emails):
        """Add additional viewer/viewers to a feature set.

        Args:
            user_emails: (list[str]]) A collection of user emails.

        Returns:
            FeatureSet: An existing feature set with the latest information.

        Typical example:
            fs.add_viewers(["bob@h2o.ai", "alice@h2o.ai"])

        For more details:
            https://docs.h2o.ai/feature-store/latest-stable/docs/api/permissions.html#feature-set-permissions-api
        """
        return self._add_permissions(user_emails, pb.PermissionType.Viewer)

    def remove_owners(self, user_emails):
        return self._remove_permissions(user_emails, pb.PermissionType.Owner)

    def remove_editors(self, user_emails):
        return self._remove_permissions(user_emails, pb.PermissionType.Editor)

    def remove_consumers(self, user_emails):
        return self._remove_permissions(user_emails, pb.PermissionType.Consumer)

    def remove_sensitive_consumers(self, user_emails):
        return self._remove_permissions(user_emails, pb.PermissionType.SensitiveConsumer)

    def remove_viewers(self, user_emails):
        """Remove viewer/viewers from a feature set.

        Args:
            user_emails: (list[str]]) A collection of user emails.

        Returns:
            FeatureSet: An existing feature set with the latest information.

        Typical example:
            fs.remove_viewers(["bob@h2o.ai", "alice@h2o.ai"])

        For more details:
            https://docs.h2o.ai/feature-store/latest-stable/docs/api/permissions.html#feature-set-permissions-api
        """
        return self._remove_permissions(user_emails, pb.PermissionType.Viewer)

    def get_active_jobs(self, job_type=pb.JobType.Unknown):
        return self._get_jobs(True, job_type)

    def _get_jobs(self, active, job_type=pb.JobType.Unknown):
        from ..collections.jobs import Jobs  # Lazy import to avoid circular reference

        request = pb.ListJobsRequest(active=active)
        request.feature_set.CopyFrom(self._feature_set)
        request.job_type = job_type
        resp = self._stub.ListJobs(request)
        return [Jobs._create_job(self._stub, job_proto) for job_proto in resp.jobs]

    def _add_permissions(self, user_emails, permission):
        request = pb.FeatureSetPermissionRequest()
        request.feature_set.CopyFrom(self._feature_set)
        request.user_emails.extend(user_emails)
        request.permission = permission
        self._stub.AddFeatureSetPermission(request)
        return self

    def _remove_permissions(self, user_emails, permission):
        request = pb.FeatureSetPermissionRequest()
        request.feature_set.CopyFrom(self._feature_set)
        request.user_emails.extend(user_emails)
        request.permission = permission
        self._stub.RemoveFeatureSetPermission(request)
        return self

    def request_access(self, access_type, reason):
        request = pb.SubmitPendingPermissionRequest()
        request.resource_id = self._feature_set.id
        request.permission = AccessType.to_proto_permission(access_type)
        request.reason = reason
        response = self._stub.SubmitPendingFeatureSetPermission(request)
        return response.permission_id

    @property
    def current_permission(self):
        request = pb.GetActivePermissionRequest(resource_id=self._feature_set.id)
        response = self._stub.GetActiveFeatureSetPermission(request)
        return AccessType.from_proto_active_permission(response.permission)

    def ingest_async(
        self,
        source,
        credentials=None,
    ):
        if self.is_derived():
            raise Exception("Manual ingest is not allowed on derived feature set")
        from ..data_source_wrappers import get_raw_data_location

        if isinstance(source, SparkDataFrame):
            source._write_to_cache(self._stub)
            data_source = source._get_cache_location()
        else:
            data_source = get_raw_data_location(source)
        request = pb.StartIngestJobRequest()
        request.feature_set.CopyFrom(self._feature_set)
        request.data_source.CopyFrom(data_source)
        CredentialsHelper.set_credentials(request, data_source, credentials)
        job_id = self._stub.StartIngestJob(request)
        return IngestJob(self._stub, job_id)

    @interactive_console.record_stats
    def ingest(
        self,
        source,
        credentials=None,
    ):
        job = self.ingest_async(source, credentials)
        result = job.wait_for_result()
        self._feature_set = result._get_feature_set()
        return result

    def materialize_online_async(self):
        request = pb.StartMaterializationOnlineRequest()
        request.feature_set.CopyFrom(self._feature_set)
        job_id = self._stub.StartMaterializationOnlineJob(request)
        return MaterializationOnlineJob(self._stub, job_id)

    @interactive_console.record_stats
    def materialize_online(self):
        job = self.materialize_online_async()
        return job.wait_for_result()

    def ingest_online(self, rows):
        if self.is_derived():
            raise Exception("Manual ingest online is not allowed on derived feature set")

        if isinstance(rows, list):
            row_list = rows
        else:
            row_list = [rows]
        request = OnlineApi.OnlineIngestRequest()
        header = FeatureSetApi.FeatureSetHeader(
            project_id=self._feature_set.project_id,
            feature_set_id=self._feature_set.id,
            feature_set_version=self._feature_set.version,
        )
        request.header.CopyFrom(header)
        request.rows.extend(row_list)
        self._stub.OnlineIngest(request)

    def retrieve_online(self, *key) -> dict:
        request = OnlineApi.OnlineRetrieveRequest()
        header = FeatureSetApi.FeatureSetHeader(
            project_id=self._feature_set.project_id,
            feature_set_id=self._feature_set.id,
            feature_set_version=self._feature_set.version,
        )
        request.header.CopyFrom(header)
        request.key.extend(map(lambda x: str(x), key))
        json_row = self._stub.OnlineRetrieve(request).row
        return json.loads(json_row)

    def retrieve(self, start_date_time=None, end_date_time=None):
        return RetrieveHolder(self._stub, self._feature_set, start_date_time, end_date_time, "")

    def list_versions(self):
        request = pb.ListFeatureSetsVersionRequest()
        request.feature_set.CopyFrom(self._feature_set)
        response = self._stub.ListFeatureSetVersions(request)
        return [VersionDescription(version) for version in response.versions]

    @property
    def schema(self):
        return FeatureSetSchema(self._stub, self)

    def ingest_history(self):
        return IngestHistory(self._stub, self._feature_set)

    def get_recommendations(self):
        request = pb.GetRecommendationRequest()
        request.feature_set.CopyFrom(self._feature_set)
        response = self._stub.GetRecommendations(request)
        return [Recommendation(self._stub, self, item) for item in response.matches]

    def schedule_ingest(self, name: str, source, schedule: str, description: str = "", credentials=None):
        from ..data_source_wrappers import get_raw_data_location

        if isinstance(source, SparkDataFrame):
            raise Exception("Scheduling Ingest with SparkDataFrame is not supported.")
        else:
            data_source = get_raw_data_location(source)

        client_timezone = datetime.datetime.utcnow().astimezone().tzname()

        request = pb.ScheduleTaskRequest(
            name=name,
            description=description,
            feature_set_id=self._feature_set.id,
            project_id=self._feature_set.project_id,
            source=data_source,
            schedule=schedule,
            feature_set_version=self._feature_set.version,
            crone_time_zone=client_timezone,
        )
        CredentialsHelper.set_credentials(request, data_source, credentials)
        scheduled_task = ScheduledTasks(self._stub, self)
        return scheduled_task.create_ingest_task(request)

    @property
    def schedule(self):
        return ScheduledTasks(self._stub, self)

    def get_preview(self):
        request = pb.GetFeatureSetPreviewRequest(
            feature_set_id=self._feature_set.id,
            feature_set_version=self._feature_set.version,
        )
        response = self._stub.GetFeatureSetPreview(request)
        if response.preview_url:
            json_response = Utils.fetch_preview_as_json_array(response.preview_url)
            return json_response
        else:
            print("No preview available. Job will be started to generate it.")
            job_id = self._start_preview_job()
            info = JobInfo(self._stub, job_id)
            while not self._get_job(job_id).done:
                info.show_progress()
                time.sleep(2)
            info.show_progress()
            return self.get_preview()

    def ingest_lazy(self, source, credentials=None):
        from ..data_source_wrappers import get_raw_data_location

        if isinstance(source, SparkDataFrame):
            raise Exception("Lazy Ingest with SparkDataFrame is not supported.")
        else:
            data_source = get_raw_data_location(source)
        request = pb.ScheduleTaskRequest(
            feature_set_id=self._feature_set.id,
            project_id=self._feature_set.project_id,
            source=data_source,
            feature_set_version=self._feature_set.version,
        )
        CredentialsHelper.set_credentials(request, data_source, credentials)
        scheduled_task = ScheduledTasks(self._stub, self)
        scheduled_task.create_lazy_ingest_task(request)
        print(f"Lazy ingest scheduled for feature set {self._feature_set.id}")

    @property
    def owners(self):
        request = pb.GetOwnersRequest(resource_id=self._feature_set.id)
        response = self._stub.GetFeatureSetOwners(request)
        return [User(owner) for owner in response.owners]

    def _start_preview_job(self):
        request = pb.PreviewRequest()
        request.feature_set.CopyFrom(self._feature_set)
        return self._stub.StartPreviewJob(request)

    def _get_job(self, job_id):
        return self._stub.GetJob(job_id)

    def __repr__(self):
        return Utils.pretty_print_proto(self._feature_set)

    def __str__(self):
        return (
            f"Feature set name    : {self.feature_set_name} \n"
            f"Description         : {self.description} \n"
            f"Version             : {self.version} \n"
            f"Secret              : {self.secret} \n"
            f"Author                \n{Utils.output_indent_spacing(str(self.author), '      ')}"
            f"Project name        : {self.project} \n"
            f"Primary key         : {self.primary_key} \n"
            f"Feature set type    : {self.feature_set_type} \n"
            f"Created             : {self.created_date_time} \n"
            f"Last updated        : {self.last_update_date_time} \n"
            f"Sensitive           : {self.special_data._fs._feature_set.special_data.sensitive} \n"
            f"Time travel column  : {self.time_travel_column} \n"
            f"Features            : {self._custom_feature_fields()} \n"
            f"Tags                : {self.tags} \n"
            f"Partition by        : {self.partition_by} \n"
            f"Feature classifiers : {self.feature_classifiers} \n"
        )

    def _custom_feature_fields(self):
        tmp_dict = dict()
        for feature in self.features:
            tmp_dict.update({feature: self.features.get(feature).data_type})
        return json.dumps(tmp_dict, indent=5)


class VersionDescription:
    def __init__(self, version_description):
        self._version_description = version_description

    def __repr__(self):
        return Utils.pretty_print_proto(self._version_description)

    def __str__(self):
        return (
            f"Version           : {Utils.proto_to_dict(self._version_description).get('version')} \n"
            f"Version change    : {Utils.proto_to_dict(self._version_description).get('version_change')} \n"
            f"Created           : {Utils.proto_to_dict(self._version_description).get('created_date_time')} \n"
        )


class TimeToLive:
    def __init__(self, stub, feature_set):
        self._stub = stub
        self._fs = feature_set

    @property
    def ttl_offline(self):
        return self._fs._feature_set.time_to_live.ttl_offline

    @ttl_offline.setter
    def ttl_offline(self, value):
        update_request = pb.UpdateFeatureSetRequest(
            feature_set_id=self._fs._feature_set.id,
            feature_set_version=self._fs._feature_set.version,
            time_to_live_offline_interval=value,
            fields_to_update=[pb.FEATURE_SET_TTL_OFFLINE],
        )
        self._fs._feature_set = self._stub.UpdateFeatureSet(update_request).updated_feature_set

    @property
    def ttl_offline_interval(self):
        return TimeToLiveApi.Offline.TimeToLiveInterval.Name(self._fs._feature_set.time_to_live.ttl_offline_interval)

    @ttl_offline_interval.setter
    def ttl_offline_interval(self, value):
        valid_units = TimeToLiveApi.Offline.TimeToLiveInterval.keys()
        if value.upper() in valid_units:
            update_request = pb.UpdateFeatureSetRequest(
                feature_set_id=self._fs._feature_set.id,
                feature_set_version=self._fs._feature_set.version,
                time_to_live_offline_interval_unit=TimeToLiveApi.Offline.TimeToLiveInterval.Value(value.upper()),
                fields_to_update=[pb.FEATURE_SET_TTL_OFFLINE_INTERVAL],
            )
            self._fs._feature_set = self._stub.UpdateFeatureSet(update_request).updated_feature_set
        else:
            raise Exception(
                "Invalid offline time to live interval unit. Supported values are: " + ", ".join(map(str, valid_units))
            )

    @property
    def ttl_online(self):
        return self._fs._feature_set.time_to_live.ttl_online

    @ttl_online.setter
    def ttl_online(self, value):
        update_request = pb.UpdateFeatureSetRequest(
            feature_set_id=self._fs._feature_set.id,
            feature_set_version=self._fs._feature_set.version,
            time_to_live_online_interval=value,
            fields_to_update=[pb.FEATURE_SET_TTL_ONLINE],
        )
        self._fs._feature_set = self._stub.UpdateFeatureSet(update_request).updated_feature_set

    @property
    def ttl_online_interval(self):
        return TimeToLiveApi.Online.TimeToLiveInterval.Name(self._fs._feature_set.time_to_live.ttl_online_interval)

    @ttl_online_interval.setter
    def ttl_online_interval(self, value):
        valid_units = TimeToLiveApi.Online.TimeToLiveInterval.keys()
        if value.upper() in valid_units:
            update_request = pb.UpdateFeatureSetRequest(
                feature_set_id=self._fs._feature_set.id,
                feature_set_version=self._fs._feature_set.version,
                time_to_live_online_interval_unit=TimeToLiveApi.Online.TimeToLiveInterval.Value(value.upper()),
                fields_to_update=[pb.FEATURE_SET_TTL_ONLINE_INTERVAL],
            )
            self._fs._feature_set = self._stub.UpdateFeatureSet(update_request).updated_feature_set
        else:
            raise Exception(
                "Invalid online time to live interval unit. Supported values are: " + ", ".join(map(str, valid_units))
            )

    def __repr__(self):
        return Utils.pretty_print_proto(self._fs._feature_set.time_to_live)

    def __str__(self):
        return (
            f"ttl offline           : {self.ttl_offline} \n"
            f"ttl online            : {self.ttl_online} \n"
            f"ttl offline interval  : {self.ttl_offline_interval} \n"
            f"ttl online interval   : {self.ttl_online_interval} \n"
        )


class FeatureSetScope:
    def __init__(self, feature_set):
        self._feature_set = feature_set
        self._scope = self._feature_set.time_travel_scope

    @property
    def start_date_time(self):
        return Utils.timestamp_to_string(self._scope.start_date_time)

    @property
    def end_date_time(self):
        return Utils.timestamp_to_string(self._scope.end_date_time)

    def __repr__(self):
        return Utils.pretty_print_proto(self._scope)

    def __str__(self):
        return f"Start date & time : {self.start_date_time} \n" f"End date & time   : {self.end_date_time} \n"


class FeatureSetSpecialData:
    def __init__(self, stub, feature_set):
        self._stub = stub
        self._fs = feature_set

    @property
    def spi(self):
        return self._fs._feature_set.special_data.spi

    @property
    def pci(self):
        return self._fs._feature_set.special_data.pci

    @property
    def rpi(self):
        return self._fs._feature_set.special_data.rpi

    @property
    def demographic(self):
        return self._fs._feature_set.special_data.demographic

    @property
    def legal(self):
        return Legal(self._stub, self._fs)

    def __repr__(self):
        return Utils.pretty_print_proto(self._fs._feature_set.special_data)

    def __str__(self):
        return (
            f"legal           \n{Utils.output_indent_spacing(str(self.legal), '    ')}"
            f"spi           : {self.spi} \n"
            f"pci           : {self.pci} \n"
            f"rpi           : {self.rpi} \n"
            f"demographic   : {self.demographic} \n"
            f"sensitive     : {Utils.proto_to_dict(self._fs._feature_set.special_data).get('sensitive')} \n"
        )


class Statistics:
    def __init__(self, feature_set):
        self._feature_set = feature_set
        self._statistics = self._feature_set.statistics

    @property
    def data_latency(self):
        return self._statistics.data_latency

    def __repr__(self):
        return Utils.pretty_print_proto(self._statistics)

    def __str__(self):
        return f"Data latency  : {self.data_latency} \n"


class Legal:
    def __init__(self, stub, feature_set):
        self._stub = stub
        self._fs = feature_set

    @property
    def approved(self):
        return self._fs._feature_set.special_data.legal.approved

    @approved.setter
    def approved(self, value):
        update_request = pb.UpdateFeatureSetRequest(
            feature_set_id=self._fs._feature_set.id,
            feature_set_version=self._fs._feature_set.version,
            legal_approved=value,
            fields_to_update=[pb.FEATURE_SET_SPECIAL_DATA_LEGAL_APPROVED],
        )
        self._fs._feature_set = self._stub.UpdateFeatureSet(update_request).updated_feature_set

    @property
    def approved_date(self):
        return Utils.timestamp_to_string(self._fs._feature_set.special_data.legal.approved_date)

    @property
    def notes(self):
        return self._fs._feature_set.special_data.legal.notes

    @notes.setter
    def notes(self, value):
        update_request = pb.UpdateFeatureSetRequest(
            feature_set_id=self._fs._feature_set.id,
            feature_set_version=self._fs._feature_set.version,
            legal_approved_notes=value,
            fields_to_update=[pb.FEATURE_SET_SPECIAL_DATA_LEGAL_NOTES],
        )
        self._fs._feature_set = self._stub.UpdateFeatureSet(update_request).updated_feature_set

    def __repr__(self):
        return Utils.pretty_print_proto(self._fs._feature_set.special_data.legal)

    def __str__(self):
        return f"Approved  : {self.approved} \n" f"Notes     : {self.notes} \n"


class Online:
    def __init__(self, feature_set):
        self._feature_set = feature_set
        self._online = self._feature_set.online

    @property
    def online_namespace(self):
        return self._online.online_namespace

    @property
    def connection_type(self):
        return self._online.connection_type

    @property
    def topic(self):
        return self._online.topic

    def __repr__(self):
        return Utils.pretty_print_proto(self._online)

    def __str__(self):
        return (
            f"Online namespace  : {self.online_namespace} \n"
            f"Connection type   : {self.connection_type} \n"
            f"Topic             : {self.topic} \n"
        )
