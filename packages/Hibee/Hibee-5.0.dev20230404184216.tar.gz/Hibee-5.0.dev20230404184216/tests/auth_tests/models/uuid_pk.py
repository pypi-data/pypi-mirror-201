import uuid

from hibeecontrib.auth.models import AbstractUser
from hibeedb import models

from .custom_user import RemoveGroupsAndPermissions

with RemoveGroupsAndPermissions():

    class UUIDUser(AbstractUser):
        """A user with a UUID as primary key"""

        id = models.UUIDField(default=uuid.uuid4, primary_key=True)
