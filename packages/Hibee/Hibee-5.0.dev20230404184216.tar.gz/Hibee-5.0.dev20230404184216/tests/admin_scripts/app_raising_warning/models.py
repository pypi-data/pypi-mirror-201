from hibeecore import checks
from hibeedb import models


class ModelRaisingMessages(models.Model):
    @classmethod
    def check(self, **kwargs):
        return [checks.Warning("A warning")]
