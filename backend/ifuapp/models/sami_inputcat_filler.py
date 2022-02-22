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

class SamiInputcatFiller(models.Model):
    """
    This group contains catalogue data derived from non-SAMI data

    Column description taken from https://datacentral.org.au/services/schema/#sami.
    """
    catid = models.BigIntegerField(primary_key=True, help_text="SAMI Galaxy ID")
    ra_obj = models.FloatField(blank=True, null=True, help_text="J2000 Right Ascension of object (deg)")
    dec_obj = models.FloatField(blank=True, null=True, help_text="J2000 Declination of object (deg)")
    z_spec = models.FloatField(blank=True, null=True, help_text="Spectroscopic redshift")
    fillflag = models.IntegerField(blank=True, null=True, help_text="Flag for different filler classes")

    class Meta:
        managed = False
        db_table = 'sami_inputcat_filler'
