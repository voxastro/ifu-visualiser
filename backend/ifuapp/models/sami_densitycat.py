import numpy as np
from django.db import models

from rest_framework import serializers, viewsets, pagination, response
from rest_flex_fields import FlexFieldsModelSerializer
from silk.profiling.profiler import silk_profile
import serpy

from ifuapp.pagination import EnhancedPageNumberPagination
from ifuapp.utils import npl

class SamiDensityCat(models.Model):
    """
    5th nearest neighbour surface density estimates.

    Column description taken from https://datacentral.org.au/services/schema/#sami.
    """
    catid = models.BigIntegerField(primary_key=True, help_text="SAMI Galaxy ID")
    surfacedensity = models.FloatField(blank=True, null=True, help_text="5th nearest neighbour surface density estimate (Mpc^-2)")
    surfacedensity_err = models.FloatField(blank=True, null=True, help_text="Surface density uncertainty (Mpc^-2)")
    completenesscorrection = models.FloatField(blank=True, null=True, help_text="Multiplicative factor correcting SurfaceDensity for spectroscopic completenes")
    areacorrection = models.FloatField(blank=True, null=True, help_text="Multiplicative factor correcting SurfaceDensity for smaller area due to edge effects")
    surfacedensityflag = models.IntegerField(blank=True, null=True, help_text="Flag indicating problems with surface density measurement")
    surfacedensity_m19 = models.FloatField(blank=True, null=True, help_text="Same as SurfaceDensity, but for Mr < -19. (Mpc^-2)")
    surfacedensity_err_m19 = models.FloatField(blank=True, null=True, help_text="Same as SurfaceDensity_err, but for Mr < -19. (Mpc^-2)")
    completenesscorrection_m19 = models.FloatField(blank=True, null=True, help_text="Same as CompletenessCorrection, but for Mr < -19.")
    areacorrection_m19 = models.FloatField(blank=True, null=True, help_text="Same as AreaCorrection, but for Mr < -19.")
    surfacedensityflag_m19 = models.IntegerField(blank=True, null=True, help_text="Same as SurfaceDensityFlag, but for Mr < -19.")

    class Meta:
        managed = False
        db_table = 'sami_densitycat'
