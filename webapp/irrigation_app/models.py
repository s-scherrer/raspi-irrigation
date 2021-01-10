from django.db import models


class Observable(models.Model):
    """
    A variable that can be observed.

    These should be only provided via fixtures.
    """
    name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=10)
    unit = models.CharField(max_length=20)


class Measurement(models.Model):
    """A measurement value read from the arduino"""
    time = models.DateTimeField("measurement time")
    observable = models.ForeignKey(Observable, on_delete=models.PROTECT)
    value = models.FloatField()
