from hibeedb import models


class Person(models.Model):
    name = models.CharField(max_length=255)
