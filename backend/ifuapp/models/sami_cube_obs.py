import numpy as np
from django.db import models

from rest_framework import serializers, viewsets, pagination, response
from rest_flex_fields import FlexFieldsModelSerializer
from silk.profiling.profiler import silk_profile
import serpy

from ifuapp.pagination import EnhancedPageNumberPagination
from ifuapp.utils import npl


class SamiCubeObs(models.Model):
    """
    SAMI cube observations, quality and flagging catalogue.

    Column description taken from https://datacentral.org.au/services/schema/#sami.
    """
    cubeidpub = models.CharField(
        primary_key=True, max_length=14, help_text="Public unique cube ID for data release")
    cubeid = models.CharField(
        max_length=80, blank=True, null=True, help_text="Internal unique cube ID")
    cubename = models.CharField(max_length=80, blank=True, null=True,
                                help_text="Internal unique cube name for blue cube")
    catid = models.BigIntegerField(
        blank=True, null=True, help_text="SAMI Galaxy ID")
    cubefwhm = models.FloatField(
        blank=True, null=True, help_text="FWHM of PSF in cube [arcsec]")
    cubetexp = models.FloatField(
        blank=True, null=True, help_text="Total exposure time for cube [sec]")
    meantrans = models.FloatField(
        blank=True, null=True, help_text="Mean transmission for cube")
    isbest = models.BooleanField(
        blank=True, null=True, help_text="Flag to indicate best repeat")
    catsource = models.IntegerField(
        blank=True, null=True, help_text="Flag to identify input source catalogue")
    warnstar = models.IntegerField(
        blank=True, null=True, help_text="Flag to indicate that object is a calibration star")
    warnfill = models.IntegerField(
        blank=True, null=True, help_text="Flag to indicate that object is from a filler catalogue")
    warnz = models.IntegerField(
        blank=True, null=True, help_text="Flag to indicate potential error in input catalogue redshift")
    warnmult = models.IntegerField(
        blank=True, null=True, help_text="Flag to indicate multiple objects within IFU field-of-view")
    warnakpc = models.IntegerField(
        blank=True, null=True, help_text="Flag to indicate 3kpc aperture spectra are missing")
    warnare = models.IntegerField(
        blank=True, null=True, help_text="Flag to indicate large difference between MGE and Sersic effective radius")
    warnamge = models.IntegerField(
        blank=True, null=True, help_text="Flag to indicate MGE Re aperture spectra are missing")
    warnsk2m = models.IntegerField(
        blank=True, null=True, help_text="Flag to indicate 2-moment stellar kinematics are missing")
    warnsk4m = models.IntegerField(
        blank=True, null=True, help_text="Flag to indicate 4-moment stellar kinematics are missing")
    warnsk4mhsn = models.IntegerField(
        blank=True, null=True, help_text="Flag to indicate high-S/N binned 4-moment stellar kinematics are missing")
    warnfcal = models.IntegerField(
        blank=True, null=True, help_text="Flag to indicate flux calibration issues")
    warnfcbr = models.IntegerField(
        blank=True, null=True, help_text="Flag to indicate flux calibration issues with offset between red and blue arm")
    warnskyb = models.IntegerField(
        blank=True, null=True, help_text="Flag to indicate excess sky subtraction residuals in blue arm")
    warnskyr = models.IntegerField(
        blank=True, null=True, help_text="Flag to indicate excess sky subtraction residuals in red arm")
    warnsker = models.IntegerField(
        blank=True, null=True, help_text="Flag to indicate problem with stellar kinematics")
    warnwcs = models.IntegerField(
        blank=True, null=True, help_text="Flag to indicate target galaxy is offset from centre of cube")
    warnre = models.IntegerField(
        blank=True, null=True, help_text="Flag to indicate large difference between MGE and Sersic effective radius")
    warnskem = models.IntegerField(
        blank=True, null=True, help_text="Flag to indicate possible impact of sky lines on emission line fitting")
    warnemft = models.IntegerField(
        blank=True, null=True, help_text="Flag to indicate missing emission line fits")

    class Meta:
        managed = False
        db_table = 'sami_cube_obs'
