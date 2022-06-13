import numpy as np
from django.db import models

from rest_framework import serializers, viewsets, pagination, response
from rest_flex_fields import FlexFieldsModelSerializer
from silk.profiling.profiler import silk_profile
import serpy

from ifuapp.pagination import EnhancedPageNumberPagination
from ifuapp.utils import npl


class SamiInputcatClusters(models.Model):
    """
    SAMI input catalogue for cluster regions.

    Column description taken from https://datacentral.org.au/services/schema/#sami.
    """
    catid = models.BigIntegerField(primary_key=True, help_text="SAMI Galaxy ID")
    ra_obj = models.FloatField(blank=True, null=True, help_text="J2000 Right Ascension of object (deg)")
    dec_obj = models.FloatField(blank=True, null=True, help_text="J2000 Declination of object (deg)")
    r_petro = models.FloatField(blank=True, null=True, help_text="Extinction-corrected r-band Petrosian mag")
    r_auto = models.FloatField(blank=True, null=True, help_text="r-band SExtractor auto magnitude")
    z_spec = models.FloatField(blank=True, null=True, help_text="Spectroscopic redshift")
    m_r = models.FloatField(blank=True, null=True, help_text="Absolute r-band magnitude")
    r_e = models.FloatField(blank=True, null=True, help_text="r-band major axis effective radius (arcsec)")
    mu_within_1re = models.FloatField(blank=True, null=True, help_text="Mean r-band surface brightness within 1 effective radius (mag/arcsec^2)")
    mu_1re = models.FloatField(blank=True, null=True, help_text="r-band surface brightness at 1 effective radius (mag/arcsec^2)")
    mu_2re = models.FloatField(blank=True, null=True, help_text="r-band surface brightness at 2 effective radii (mag/arcsec^2)")
    ellip = models.FloatField(blank=True, null=True, help_text="r-band ellipticity")
    pa = models.FloatField(blank=True, null=True, help_text="r-band position angle (deg)")
    g_i = models.FloatField(blank=True, null=True, help_text="(g-i) colour")
    mstar = models.FloatField(blank=True, null=True, help_text="Logarithm of stellar mass (dex)")
    r_on_rtwo = models.FloatField(blank=True, null=True, help_text="Projected distance from cluster centre normalised by R200")
    v_on_sigma = models.FloatField(blank=True, null=True, help_text="Line-of-sight velocity relative to cluster redshift normalised by cluster velocity dispersion measured within R200")
    is_mem = models.BooleanField(blank=True, null=True, help_text="Flag indicating cluster membership (1=member, 0=non-member)")
    surv_sami = models.IntegerField(blank=True, null=True, help_text="Priority class for targets")
    bad_class = models.IntegerField(blank=True, null=True, help_text="Flag for bad or problem objects")

    class Meta:
        managed = False
        db_table = 'sami_inputcat_clusters'
