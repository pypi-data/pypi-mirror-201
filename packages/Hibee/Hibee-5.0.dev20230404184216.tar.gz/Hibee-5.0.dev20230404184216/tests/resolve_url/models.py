"""
Regression tests for the resolve_url function.
"""

from hibeedb import models


class UnimportantThing(models.Model):
    importance = models.IntegerField()

    def get_absolute_url(self):
        return "/importance/%d/" % self.importance
