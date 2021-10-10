import numpy as np
from django.db import models

from rest_framework import serializers, viewsets
from rest_flex_fields import FlexFieldsModelSerializer

import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType
from graphene_django_pagination import DjangoPaginationConnectionField

from ifuapp.utils import npl
from ifuapp.pagination import EnhancedPageNumberPagination

from ..utils import apply_search


class Cube(models.Model):
    """
    The main table of spectral cubes.
    """
    cube_id = models.IntegerField(
        primary_key=True, help_text="Primary ID of the spectral cube.")
    ra = models.FloatField(blank=True, null=True,
                           help_text="Right Accession coordinate of the center of the "
                           "cube's field of view. Extracted from the cube WCS, except "
                           "for the Atlas3D survey, where the coordinates are taken from "
                           "the fits header.")
    dec = models.FloatField(blank=True, null=True, help_text="Declination coordinate of the center of the "
                            "cube's field of view. Extracted from the cube WCS, except "
                            "for the Atlas3D survey, where the coordinates are taken from "
                            "the fits header.")
    survey = models.CharField(max_length=32, blank=True, null=True,
                              help_text="Survey name")
    filename = models.CharField(max_length=64, blank=True, null=True,
                                help_text="File name of the spectral cube.")
    exptime = models.FloatField(blank=True, null=True,
                                help_text='Total exposure time extracted from spectral cube.')
    manga_id = models.CharField(max_length=32, blank=True, null=True,
                                help_text="MaNGA ID identifier of MaNGA survey target")
    manga_plateifu = models.CharField(max_length=32, blank=True, null=True,
                                      help_text="Plate-IFU identifier of MaNGA survey target")
    sami_catid = models.BigIntegerField(blank=True, null=True,
                                        help_text="'catid' identifier of SAMI survey target")
    sami_cubeidpub = models.CharField(max_length=32, blank=True, null=True,
                                      help_text="'cube' identifier of SAMI survey target. "
                                      "Used as part of the cube filename.")
    califa_id = models.IntegerField(blank=True, null=True,
                                    help_text="'id' identifier of Califa survey target")
    califa_name = models.CharField(max_length=32, blank=True, null=True,
                                   help_text="Galaxy name of Califa survey target")
    califa_cube = models.CharField(max_length=32, blank=True, null=True,
                                   help_text="Cube type of Califa survey target")
    atlas_name = models.CharField(max_length=32, blank=True, null=True,
                                  help_text="Galaxy name of Atlas3D survey target")

    atlas_param = models.ForeignKey(
        'AtlasParam', models.DO_NOTHING, db_column='atlas_param', blank=True, null=True,
        related_name='cubes', related_query_name='cubes')
    atlas_morphkin = models.ForeignKey(
        'AtlasMorphkin', models.DO_NOTHING, db_column='atlas_morphkin', blank=True,
        null=True, related_name='cubes', related_query_name='cubes')
    califa_object = models.ForeignKey(
        'CalifaObject', models.DO_NOTHING, db_column='califa_object', blank=True,
        null=True, related_name='cubes', related_query_name='cubes')
    sami_cube_obs = models.ForeignKey('SamiCubeObs', models.DO_NOTHING,
                                      db_column='sami_cube_obs', blank=True, null=True,
                                      related_name='cubes', related_query_name='cubes')
    sami_inputcat_gama = models.ForeignKey('SamiInputcatGama', models.DO_NOTHING,
                                           db_column='sami_inputcat_gama', blank=True, null=True,
                                           related_name='cubes', related_query_name='cubes')
    manga_drp = models.ForeignKey('MangaDrp', models.DO_NOTHING,
                                  db_column='manga_drp', blank=True, null=True,
                                  related_name='cubes', related_query_name='cubes')

    class Meta:
        managed = False
        db_table = 'cube'

    def __str__(self):
        return f"{self.survey} - {self.cube_id}"

    def get_spectrum(self):
        """Test model method"""
        spec = np.random.random(100)
        err = np.random.random(100)

        return dict(spec=npl(spec), err=npl(err), meta=dict(objname="SomeGalaxy", header=None))
