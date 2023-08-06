import ai.h2o.featurestore.api.v1.CoreService_pb2 as pb

from .permission_base import PermissionBase
from .user import User


class Permission(PermissionBase):
    @property
    def user(self):
        return User(self._permission.user)


class ManageablePermission(Permission):
    @property
    def requestor(self):
        return User(self._permission.user)

    def revoke(self, reason):
        request = pb.RevokePermissionRequest(permission_id=self._permission.id, reason=reason)
        self._stub.RevokePermission(request)
