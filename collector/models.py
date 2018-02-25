# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField

class RawData(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    ref_url = models.URLField(unique=True)
    stage = models.IntegerField(default=0)

    class Meta:
        abstract = True  # Set this model as Abstract


# Create your models here.
class ShellData(RawData):
    title = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=30, blank=True), blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

# class TaobaoData(RawData):