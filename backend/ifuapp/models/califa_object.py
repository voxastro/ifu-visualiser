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


class CalifaObject(models.Model):
    """
    Object data for Califa DR3 sample.

    Table was derived from TAP service http://dc.zah.uni-heidelberg.de/tap using ADQL query `SELECT * FROM califadr3.objects`
    """
    califa_id = models.IntegerField(primary_key=True, unique=True,
                                    help_text="CALIFA internal object key")
    target_name = models.CharField(
        max_length=23, blank=True, null=True, help_text="Object a targeted observation")
    raj2000 = models.FloatField(
        blank=True, null=True, help_text="Right ascension of the galaxy center, J2000 (from NED) [deg]")
    dej2000 = models.FloatField(
        blank=True, null=True, help_text="Right ascension of the galaxy center, J2000 (from NED) [deg]")
    redshift = models.FloatField(
        blank=True, null=True, help_text="Redshift, from growth curve analysis photometry for mother sample galaxies, from SDSS DR7/12 petrosian photometry otherwise.")
    sdss_z = models.FloatField(
        blank=True, null=True, help_text="Redshift taken from SDSS DR7")
    maj_axis = models.FloatField(
        blank=True, null=True, help_text="Apparent isophotal major axis from SDSS [arcsec]")
    mstar = models.FloatField(blank=True, null=True,
                              help_text="Stellar mass [log(solMass)]")
    mstar_min = models.FloatField(
        blank=True, null=True, help_text="3 sigma lower limit of Stellar mass [log(solMass)]")
    mstar_max = models.FloatField(
        blank=True, null=True, help_text="3 sigma upper limit of Stellar mass [log(solMass)]")
    chi2 = models.FloatField(blank=True, null=True,
                             help_text="Chi2 of best fit")
    vmax_nocorr = models.FloatField(
        blank=True, null=True, help_text="Survey volume for this galaxy from apparent isophotal diameter and measured redshift (cf. 2014A&A...569A...1W) [Mpc**3]")
    vmax_denscorr = models.FloatField(
        blank=True, null=True, help_text="V_max additionally corrected for cosmic variance (cf. 2014A&A...569A...1W) [Mpc**3]")
    magu = models.FloatField(
        blank=True, null=True, help_text="Magnitude in the u band. This is from a growth curve analysis of the SDSS imagery for galaxies in the mother sample (id<1000). Otherwiese, it is the SDSS DR7/12 petrosian magnitude.")
    err_magu = models.FloatField(
        blank=True, null=True, help_text="Error in m_u")
    u_ext = models.FloatField(blank=True, null=True,
                              help_text="Extinction in the u band")
    abs_u_min = models.FloatField(
        blank=True, null=True, help_text="3 sigma lower limit of the absolute magnitude in u")
    abs_u_max = models.FloatField(
        blank=True, null=True, help_text="3 sigma upper limit of the absolute magnitude in u")
    magg = models.FloatField(
        blank=True, null=True, help_text="Magnitude in the g band. This is from a growth curve analysis of the SDSS imagery for galaxies in the mother sample (id<1000). Otherwiese, it is the SDSS DR7/12 petrosian magnitude.")
    err_magg = models.FloatField(
        blank=True, null=True, help_text="Error in m_g")
    g_ext = models.FloatField(blank=True, null=True,
                              help_text="Extinction in the g band")
    abs_g_min = models.FloatField(
        blank=True, null=True, help_text="3 sigma lower limit of the absolute magnitude in g")
    abs_g_max = models.FloatField(
        blank=True, null=True, help_text="3 sigma upper limit of the absolute magnitude in g")
    magr = models.FloatField(
        blank=True, null=True, help_text="Magnitude in the r band. This is from a growth curve analysis of the SDSS imagery for galaxies in the mother sample (id<1000). Otherwiese, it is the SDSS DR7/12 petrosian magnitude.")
    err_magr = models.FloatField(
        blank=True, null=True, help_text="Error in m_r")
    r_ext = models.FloatField(blank=True, null=True,
                              help_text="Extinction in the r band")
    abs_r_min = models.FloatField(
        blank=True, null=True, help_text="3 sigma lower limit of the absolute magnitude in r")
    abs_r_max = models.FloatField(
        blank=True, null=True, help_text="3 sigma upper limit of the absolute magnitude in r")
    magi = models.FloatField(
        blank=True, null=True, help_text="Magnitude in the i band. This is from a growth curve analysis of the SDSS imagery for galaxies in the mother sample (id<1000). Otherwiese, it is the SDSS DR7/12 petrosian magnitude.")
    err_magi = models.FloatField(
        blank=True, null=True, help_text="Error in m_i")
    i_ext = models.FloatField(blank=True, null=True,
                              help_text="Extinction in the i band")
    abs_i_min = models.FloatField(
        blank=True, null=True, help_text="3 sigma lower limit of the absolute magnitude in i")
    abs_i_max = models.FloatField(
        blank=True, null=True, help_text="3 sigma upper limit of the absolute magnitude in i")
    magz = models.FloatField(
        blank=True, null=True, help_text="Magnitude in the z band. This is from a growth curve analysis of the SDSS imagery for galaxies in the mother sample (id<1000). Otherwiese, it is the SDSS DR7/12 petrosian magnitude.")
    err_magz = models.FloatField(
        blank=True, null=True, help_text="Error in m_z")
    z_ext = models.FloatField(blank=True, null=True,
                              help_text="Extinction in the z band")
    abs_z_min = models.FloatField(
        blank=True, null=True, help_text="3 sigma lower limit of the absolute magnitude in z")
    abs_z_max = models.FloatField(
        blank=True, null=True, help_text="3 sigma upper limit of the absolute magnitude in z")
    hubtyp = models.CharField(max_length=16, blank=True, null=True,
                              help_text="Morphological type from CALIFA's own visual classification (see 2014A&A...569A...1W for details). (M) indicates definite merging going on, (m) indicates likely merging, (i) indicates signs of interaction.")
    minhubtyp = models.CharField(max_length=16, blank=True, null=True,
                                 help_text="Earliest morphological type in CALIFA's estimation")
    maxhubtyp = models.CharField(max_length=16, blank=True, null=True,
                                 help_text="Latest morphological type in CALIFA's estimation")
    bar = models.CharField(max_length=16, blank=True, null=True,
                           help_text="Bar strength, A -- strong bar, AB -- intermediate, B -- weak bar; with minimum and maximum estimates.")
    flag_release_comb = models.BooleanField(
        blank=True, null=True, help_text="Cube in setup COMB available?")
    flag_release_v1200 = models.BooleanField(
        blank=True, null=True, help_text="Cube in setup V1200 available?")
    flag_release_v500 = models.BooleanField(
        blank=True, null=True, help_text="Cube in setup V500 available?")
    axis_ratio = models.FloatField(
        blank=True, null=True, help_text="b/a axis ratio of a moment-based anaylsis of the SDSS DR7 images (cf. 2014A&A...569A...1W).")
    position_angle = models.FloatField(
        blank=True, null=True, help_text="Position angle wrt north. [deg]")
    el_hlr = models.FloatField(
        blank=True, null=True, help_text="Petrosian half-light radius in r band [arcsec]")
    modmag_r = models.FloatField(
        blank=True, null=True, help_text="Model magnitude in r band [mag]")

    class Meta:
        managed = False
        db_table = 'califa_object'
