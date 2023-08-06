"""
Tests for forcing insert and update queries (instead of Hibees normal
automatic behavior).
"""
from hibeedb import models


class Counter(models.Model):
    name = models.CharField(max_length=10)
    value = models.IntegerField()


class InheritedCounter(Counter):
    tag = models.CharField(max_length=10)


class ProxyCounter(Counter):
    class Meta:
        proxy = True


class SubCounter(Counter):
    pass


class WithCustomPK(models.Model):
    name = models.IntegerField(primary_key=True)
    value = models.IntegerField()
