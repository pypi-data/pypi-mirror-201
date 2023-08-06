from hibeedb import models


class MinimalUser(models.Model):
    REQUIRED_FIELDS = ()
    USERNAME_FIELD = "id"
