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
    SAMI input catalog based on GAMA survey.

    Column description taken from https://datacentral.org.au/services/schema/#sami.
    """
    catid = models.BigIntegerField(primary_key=True, help_text="SAMI Galaxy ID")
    ra_obj = models.FloatField(blank=True, null=True, help_text="J2000 Right Ascension of object (deg)")
    dec_obj = models.FloatField(blank=True, null=True, help_text="J2000 Declination of object (deg)")
    ra_ifu = models.FloatField(blank=True, null=True, help_text="J2000 Right Ascension of nominal IFU centre (deg)")
    dec_ifu = models.FloatField(blank=True, null=True, help_text="J2000 Declination of nominal IFU centre (deg)")
    r_petro = models.FloatField(blank=True, null=True, help_text="Extinction-corrected SDSS DR7 r-band Petrosian mag")
    r_auto = models.FloatField(blank=True, null=True, help_text="r-band SExtractor auto magnitude")
    z_tonry = models.FloatField(blank=True, null=True, help_text="Flow-corrected redshift")
    z_spec = models.FloatField(blank=True, null=True, help_text="Spectroscopic redshift")
    m_r = models.FloatField(blank=True, null=True, help_text="Absolute r-band magnitude")
    r_e = models.FloatField(blank=True, null=True, help_text="r-band major axis effective radius (arcsec)")
    mu_within_1re = models.FloatField(blank=True, null=True, help_text="Mean r-band surface brightness within 1 effective radius (mag/arcsec^2)")
    mu_1re = models.FloatField(blank=True, null=True, help_text="r-band surface brightness at 1 effective radius (mag/arcsec^2)")
    mu_2re = models.FloatField(blank=True, null=True, help_text="r-band surface brightness at 2 effective radii (mag/arcsec^2)")
    ellip = models.FloatField(blank=True, null=True, help_text="r-band ellipticity")
    pa = models.FloatField(blank=True, null=True, help_text="r-band position angle (deg)")
    mstar = models.FloatField(blank=True, null=True, help_text="Logarithm of stellar mass (dex solar masses)")
    g_i = models.FloatField(blank=True, null=True, help_text="(g-i) colour")
    a_g = models.FloatField(blank=True, null=True, help_text="g-band extinction")
    surv_sami = models.IntegerField(blank=True, null=True, help_text="Priority class for targets")
    bad_class = models.IntegerField(blank=True, null=True, help_text="Flag for bad or problem objects")

    class Meta:
        managed = False
        db_table = 'sami_inputcat_gama'
