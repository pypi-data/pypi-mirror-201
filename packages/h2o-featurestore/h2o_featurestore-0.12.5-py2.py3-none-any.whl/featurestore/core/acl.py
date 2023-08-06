import ai.h2o.featurestore.api.v1.CoreService_pb2 as pb
from featurestore.core.entities.permission import ManageablePermission, Permission
from featurestore.core.entities.permission_request import ManageablePermissionRequest, PermissionRequest


class AccessControlList:
    def __init__(self, stub):
        self.requests = AclRequests(stub)
        self.permissions = AclPermissions(stub)


class AclRequests:
    def __init__(self, stub):
        self.projects = AclProjectRequests(stub)
        self.feature_sets = AclFeatureSetsRequests(stub)


class AclPermissions:
    def __init__(self, stub):
        self.projects = AclProjectPermissions(stub)
        self.feature_sets = AclFeatureSetsPermissions(stub)


class AclProjectRequests:
    def __init__(self, stub):
        self._stub = stub

    def list(self):
        request = pb.ListPermissionsPageRequest(filters=[pb.PermissionState.PENDING])
        return (
            PermissionRequest(self._stub, entry.permission, entry.project.name)
            for entry in paged_response_to_request(request, self._stub.ListProjectPermissionsPage)
        )

    def list_manageable(self):
        request = pb.ListPermissionsPageRequest(filters=[pb.PermissionState.PENDING])
        return (
            ManageablePermissionRequest(self._stub, entry.permission, entry.project.name)
            for entry in paged_response_to_request(request, self._stub.ListManageableProjectPermissionsPage)
        )


class AclFeatureSetsRequests:
    def __init__(self, stub):
        self._stub = stub

    def list(self):
        request = pb.ListPermissionsPageRequest(filters=[pb.PermissionState.PENDING])
        return (
            PermissionRequest(self._stub, entry.permission, entry.feature_set.project_name)
            for entry in paged_response_to_request(request, self._stub.ListFeatureSetsPermissionsPage)
        )

    def list_manageable(self):
        request = pb.ListPermissionsPageRequest(filters=[pb.PermissionState.PENDING])
        return (
            ManageablePermissionRequest(self._stub, entry.permission, entry.feature_set.project_name)
            for entry in paged_response_to_request(request, self._stub.ListManageableFeatureSetsPermissionsPage)
        )


class AclProjectPermissions:
    def __init__(self, stub):
        self._stub = stub

    def list(self, filters=None):
        if filters is None:
            filters = [pb.PermissionState.GRANTED]
        request = pb.ListPermissionsPageRequest(filters=filters)
        return (
            Permission(self._stub, entry.permission, entry.project.name)
            for entry in paged_response_to_request(request, self._stub.ListProjectPermissionsPage)
        )

    def list_manageable(self, filters=None):
        if filters is None:
            filters = [pb.PermissionState.GRANTED]
        request = pb.ListPermissionsPageRequest(filters=filters)
        return (
            ManageablePermission(self._stub, entry.permission, entry.project.name)
            for entry in paged_response_to_request(request, self._stub.ListManageableProjectPermissionsPage)
        )


class AclFeatureSetsPermissions:
    def __init__(self, stub):
        self._stub = stub

    def list(self, filters=None):
        if filters is None:
            filters = [pb.PermissionState.GRANTED]
        request = pb.ListPermissionsPageRequest(filters=filters)
        return (
            Permission(self._stub, entry.permission, entry.feature_set.project_name)
            for entry in paged_response_to_request(request, self._stub.ListFeatureSetsPermissionsPage)
        )

    def list_manageable(self, filters=None):
        if filters is None:
            filters = [pb.PermissionState.GRANTED]
        request = pb.ListPermissionsPageRequest(filters=filters)
        return (
            ManageablePermission(self._stub, entry.permission, entry.feature_set.project_name)
            for entry in paged_response_to_request(request, self._stub.ListManageableFeatureSetsPermissionsPage)
        )


def paged_response_to_request(request, core_call):
    while request:
        response = core_call(request)
        if response.next_page_token:
            request.page_token = response.next_page_token
        else:
            request = None
        for entry in response.entries:
            yield entry
