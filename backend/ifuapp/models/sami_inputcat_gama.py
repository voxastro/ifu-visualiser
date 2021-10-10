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


class SamiInputcatGama(models.Model):
    """
    SAMI input catalog basedon GAMA survey.

    Column description taken from https://datacentral.org.au/services/schema/#sami.
    """
    catid = models.BigIntegerField(primary_key=True)
    ra_obj = models.FloatField(blank=True, null=True)
    dec_obj = models.FloatField(blank=True, null=True)
    ra_ifu = models.FloatField(blank=True, null=True)
    dec_ifu = models.FloatField(blank=True, null=True)
    r_petro = models.FloatField(blank=True, null=True)
    r_auto = models.FloatField(blank=True, null=True)
    z_tonry = models.FloatField(blank=True, null=True)
    z_spec = models.FloatField(blank=True, null=True)
    m_r = models.FloatField(blank=True, null=True)
    r_e = models.FloatField(blank=True, null=True)
    mu_within_1re = models.FloatField(blank=True, null=True)
    mu_1re = models.FloatField(blank=True, null=True)
    mu_2re = models.FloatField(blank=True, null=True)
    ellip = models.FloatField(blank=True, null=True)
    pa = models.FloatField(blank=True, null=True)
    mstar = models.FloatField(blank=True, null=True)
    g_i = models.FloatField(blank=True, null=True)
    a_g = models.FloatField(blank=True, null=True)
    surv_sami = models.IntegerField(blank=True, null=True)
    bad_class = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sami_inputcat_gama'
