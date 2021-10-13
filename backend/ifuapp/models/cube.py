import numpy as np
import os
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

from rest_framework import serializers, viewsets
from rest_flex_fields import FlexFieldsModelSerializer

import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType
from graphene_django_pagination import DjangoPaginationConnectionField

from ifuapp.utils import npl
from ifuapp.pagination import EnhancedPageNumberPagination

from astropy.io import fits
from astropy.wcs import WCS, utils as wutils
from astropy.coordinates import SkyCoord

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
    # This field type is a guess
    fov_fits = ArrayField(ArrayField(models.FloatField(blank=True, null=True)),
                          help_text="Coordinates of the rectangular area covered by cube fits file")

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

    def get_spectrum(self, ra=None, dec=None, arcsec_x=0.0, arcsec_y=0.0):
        """Test model method"""

        print("==============================================================")
        print(settings.IFU_PATH)

        if self.survey == 'manga':
            plate, idudsgn = self.manga_plateifu.split("-")
            file_cube = f"{settings.IFU_PATH}/manga_dr16/spectro/redux/v2_4_3/{plate}/stack/manga-{self.manga_plateifu}-LOGCUBE.fits"

            if not os.path.isfile(file_cube):
                file_cube += ".gz"

            fits.info(file_cube)
            with fits.open(file_cube) as hdul:
                hdr = hdul['FLUX'].header
                flux = hdul['FLUX'].data
                ivar = hdul['IVAR'].data
                wave = hdul['WAVE'].data

            sz = flux.shape
            w = WCS(hdr).dropaxis(-1)
            scale = np.mean(wutils.proj_plane_pixel_scales(w)*3600.0)

            if (ra != None) & (dec != None):
                coo = SkyCoord(float(ra), float(dec), unit=('deg', 'deg'))
                x, y = w.world_to_pixel(coo)
                arcsec_x = (x - sz[1]/2) * scale
                arcsec_y = (y - sz[2]/2) * scale
                pixel_x = np.round(x).astype(int)
                pixel_y = np.round(y).astype(int)
            elif (arcsec_x != None) & (arcsec_y != None):
                pixel_x = np.round(float(arcsec_x)/scale + sz[1]/2).astype(int)
                pixel_y = np.round(float(arcsec_y)/scale + sz[2]/2).astype(int)
                coo = w.pixel_to_world(float(arcsec_x), float(arcsec_y))
                ra = coo.ra.deg
                dec = coo.dec.deg

            else:
                return None

            if (0 <= pixel_x < sz[1]) & (0 <= pixel_y < sz[2]):
                flx = npl(flux[:, pixel_x, pixel_y])
                error = npl(1.0/np.sqrt(ivar[:, pixel_x, pixel_y]))
                wav = npl(wave)
                return dict(ra=ra, dec=dec, arcsec_x=arcsec_x,
                            arcsec_y=arcsec_y, pixel_x=pixel_x,
                            pixel_y=pixel_y, flux=flx, error=error, wave=wav)
            else:
                return None
