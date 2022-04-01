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


class SamiMGEPhotomUnreg(models.Model):
    """
    Results from Multi Gaussian Expansion fitting of imaging data.

    Column description taken from https://datacentral.org.au/services/schema/#sami.
    """
    ind = models.IntegerField(primary_key=True)
    catid = models.BigIntegerField(
        help_text="SAMI Galaxy ID. Galaxies with two entries have both VST and SDSS photometry.")
    photometry = models.CharField(
        blank=True, null=True, max_length=8, help_text="Denotes which images were used.")
    remge = models.FloatField(
        blank=True, null=True, help_text="Circularised effective radius from MGE fit (arcsec).")
    mmge = models.FloatField(
        blank=True, null=True, help_text="Total AB magnitude from the MGE fit. No corrections applied.")
    rextinction = models.FloatField(
        blank=True, null=True, help_text="Extinction from Schlafly+2011.")
    pamge = models.FloatField(
        blank=True, null=True, help_text="Position Angle of the MGE model, from N to E is positive (deg).")
    epsmge_re = models.FloatField(
        blank=True, null=True, help_text="Model isophotal ellipticity at one Re.")
    epsmge_lw = models.FloatField(
        blank=True, null=True, help_text="Light-weighted ellipticity of the model.")
    dist2nneigh = models.FloatField(
        blank=True, null=True, help_text="Distance to nearest neighbour from SExtractor source extraction (arcsec).")
    chi2 = models.FloatField(blank=True, null=True,
                             help_text="Chi^2 from MGE fit.")
    cube = models.ForeignKey('Cube', models.DO_NOTHING, db_column='cube',
                             blank=True, null=True, related_name="sami_mgephotom_unreg")

    class Meta:
        managed = False
        db_table = 'sami_mgephotom_unreg'
