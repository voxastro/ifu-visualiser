import numpy as np
from django.db import models

from rest_framework import serializers, viewsets, pagination, response
from rest_flex_fields import FlexFieldsModelSerializer
from silk.profiling.profiler import silk_profile
import serpy

from ifuapp.pagination import EnhancedPageNumberPagination
from ifuapp.utils import npl

import graphene
from graphene_django import DjangoObjectType, DjangoListField
from graphene.types.generic import GenericScalar
from graphene_django_pagination import DjangoPaginationConnectionField

class SamiGasKinPA(models.Model):
    """
    Gas Kinematic PA Catalogue

    Column description taken from https://datacentral.org.au/services/schema/#sami.
    """
    cubeid = models.CharField(blank=True, null=True, max_length=80, help_text="Internal unique cube ID")
    cubeidpub = models.CharField(blank=True, null=True, max_length=15, help_text="Public unique cube ID for data release")
    cubename = models.CharField(blank=True, null=True, max_length=80, help_text="Internal unique cube name for blue cube")
    catid = models.BigIntegerField(primary_key=True, help_text="SAMI Galaxy ID")
    pa_gaskin = models.FloatField(blank=True, null=True, help_text="Gas kinematic position angle. Anticlockwise, North=0 degrees (deg)")
    pa_gaskin_err = models.FloatField(blank=True, null=True, help_text="1-sigma error on the gas kinematic position angle (deg)")

    class Meta:
        managed = False
        db_table = 'sami_gaskin'
