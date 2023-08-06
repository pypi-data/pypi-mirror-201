import ai.h2o.featurestore.api.v1.CoreService_pb2 as pb

from .permission_base import PermissionBase
from .user import User


class PermissionRequest(PermissionBase):
    @property
    def user(self):
        return User(self._permission.user)


class ManageablePermissionRequest(PermissionRequest):
    @property
    def requestor(self):
        return User(self._permission.user)

    def approve(self, reason):
        request = pb.ApprovePendingPermissionRequest(permission_id=self._permission.id, reason=reason)
        self._stub.ApprovePendingPermission(request)

    def reject(self, reason):
        request = pb.RejectPendingPermissionRequest(permission_id=self._permission.id, reason=reason)
        self._stub.RejectPendingPermission(request)
