import numpy as np
import os
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

from rest_framework import serializers, viewsets
from rest_flex_fields import FlexFieldsModelSerializer

from ifuapp.utils import npl
from ifuapp.pagination import EnhancedPageNumberPagination

from astropy.io import fits
from astropy.wcs import WCS, utils as wutils, FITSFixedWarning
from astropy.coordinates import SkyCoord
import warnings
warnings.filterwarnings('ignore', category=FITSFixedWarning, append=True)


def file_check(file):
    if not os.path.isfile(file):
        file += ".gz"
    return file


def wave_hdr(hdr, index='3'):
    waves = hdr['CRVAL'+index] + hdr['CDELT'+index] * (np.arange(hdr['NAXIS'+index]) - hdr['CRPIX'+index] - 1)
    return waves


def get_pointer_coords(w, sz, ra, dec, arcsec_x, arcsec_y):
    scale = np.mean(wutils.proj_plane_pixel_scales(w)*3600.0)

    if (ra != None) & (dec != None):
        coo = SkyCoord(float(ra), float(dec), unit=('deg', 'deg'))
        x, y = w.world_to_pixel(coo)
        arcsec_x = (x - sz[0]/2) * scale
        arcsec_y = (y - sz[1]/2) * scale
        pixel_x = np.round(x).astype(int)
        pixel_y = np.round(y).astype(int)
    elif (arcsec_x != None) & (arcsec_y != None):
        pixel_x = np.round(float(arcsec_x)/scale + sz[0]/2).astype(int)
        pixel_y = np.round(float(arcsec_y)/scale + sz[1]/2).astype(int)
        coo = w.pixel_to_world(float(arcsec_x), float(arcsec_y))
        ra = coo.ra.deg
        dec = coo.dec.deg
    else:
        raise ValueError(
            "Neither ra, dec, nor arcsec_x, arcsec_y were provided.")

    return float(ra), float(dec), arcsec_x, arcsec_y, pixel_x, pixel_y


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
    bino_name = models.CharField(max_length=32, blank=True, null=True,
                                 help_text="Target name taken with Binospec-IFU")
    bino_grating = models.CharField(max_length=32, blank=True, null=True,
                                    help_text="Used disperser for Binospec-IFU observations")
    # This field type is a guess
    fov_fits = ArrayField(ArrayField(models.FloatField(blank=True, null=True)),
                          help_text="Coordinates of the rectangular area covered by cube fits file")
    fov_ifu = ArrayField(ArrayField(models.FloatField(blank=True, null=True)),
                         help_text="Coordinates of the IFU field-of-view")

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

    sami_inputcat_filler = models.ForeignKey('SamiInputcatFiller', models.DO_NOTHING,
                                             db_column='sami_inputcat_filler', blank=True, null=True,
                                             related_name='cubes', related_query_name='cubes')

    sami_densitycat = models.ForeignKey('SamiDensityCat', models.DO_NOTHING,
                                        db_column='sami_densitycat', blank=True, null=True,
                                        related_name='cubes', related_query_name='cubes')

    sami_inputcat_clusters = models.ForeignKey('SamiInputcatClusters', models.DO_NOTHING,
                                               db_column='sami_inputcat_clusters', blank=True, null=True,
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

        output = dict()
        output['ra'] = ra
        output['dec'] = dec
        output['arcsec_x'] = arcsec_x
        output['arcsec_y'] = arcsec_y
        output['pixel_x'] = None
        output['pixel_y'] = None

        if self.survey == 'manga':
            plate, idudsgn = self.manga_plateifu.split("-")
            file_cube = f"{settings.IFU_PATH}/manga_dr17/spectro/redux/MPL-11/{plate}/stack/manga-{self.manga_plateifu}-LOGCUBE.fits"
            file_cube = file_check(file_cube)

            with fits.open(file_cube) as hdul:
                hdul.verify('fix')
                hdr = hdul['FLUX'].header
                flux = hdul['FLUX'].data
                ivar = hdul['IVAR'].data
                wave = hdul['WAVE'].data

            w = WCS(hdr).dropaxis(-1)
            sz = w.pixel_shape

            ra, dec, arcsec_x, arcsec_y, pixel_x, pixel_y = \
                get_pointer_coords(w, sz, ra, dec, arcsec_x, arcsec_y)

            if (0 <= pixel_x < sz[0]) & (0 <= pixel_y < sz[1]):
                flx = flux[:, pixel_y, pixel_x]
                error = 1.0/np.sqrt(ivar[:, pixel_y, pixel_x])
                wav = wave
                yrange = [0, np.nanpercentile(flux[:, pixel_y, pixel_x], 99)]

                output['spec'] = [
                    dict(flux=npl(flx), error=npl(error), wave=npl(wav), yrange=npl(yrange))]
                output['status'] = "ok"
                output['message'] = ""
            else:
                output['spec'] = []
                output['status'] = "warning"
                output['message'] = "The point is out of the cube field-of-view."

        elif self.survey == 'sami':
            spec = []
            for suf in ['red', 'blue']:
                file_cube = f"{settings.IFU_PATH}/sami_dr3/{self.sami_catid}/{self.sami_cubeidpub}_cube_{suf}.fits"
                file_cube = file_check(file_cube)
                with fits.open(file_cube) as hdul:
                    hdr = hdul['PRIMARY'].header
                    flux = hdul['PRIMARY'].data
                    var = hdul['VARIANCE'].data
                wave = wave_hdr(hdr)

                # calculate pointer coordinates based on the first red cube.
                # Assuming both cubes are identical.
                if suf == 'red':
                    w = WCS(hdr).dropaxis(-1)
                    sz = w.pixel_shape

                    ra, dec, arcsec_x, arcsec_y, pixel_x, pixel_y = \
                        get_pointer_coords(w, sz, ra, dec, arcsec_x, arcsec_y)

                if (0 <= pixel_x < sz[0]) & (0 <= pixel_y < sz[1]):
                    flx = flux[:, pixel_y, pixel_x]
                    error = np.sqrt(var[:, pixel_y, pixel_x])
                    wav = wave
                    yrange = [0, np.nanpercentile(
                        flux[:, pixel_y, pixel_x], 99)]
                    spec.append(dict(flux=npl(flx), error=npl(error),
                                wave=npl(wav), yrange=npl(yrange)))
                    output['status'] = "ok"
                    output['message'] = ""
                else:
                    output['status'] = "warning"
                    output['message'] = "The point is out of the cube field-of-view."

            output['spec'] = spec

        elif self.survey == 'califa':
            file_cube = f"{settings.IFU_PATH}/califa_dr3/{self.califa_cube}/reduced_v2.2/{self.califa_name}.{self.califa_cube}.rscube.fits"
            file_cube = file_check(file_cube)

            with fits.open(file_cube) as hdul:
                hdr = hdul['PRIMARY'].header
                flux = hdul['PRIMARY'].data
                err = hdul['ERROR'].data

            # fix bad error values
            errmsk = err > 100*np.nanmedian(err)
            err[errmsk] = np.nan

            wave = wave_hdr(hdr)

            w = WCS(hdr).dropaxis(-1)
            sz = w.pixel_shape

            ra, dec, arcsec_x, arcsec_y, pixel_x, pixel_y = \
                get_pointer_coords(w, sz, ra, dec, arcsec_x, arcsec_y)

            if (0 <= pixel_x < sz[0]) & (0 <= pixel_y < sz[1]):
                flx = flux[:, pixel_y, pixel_x]
                error = err[:, pixel_y, pixel_x]
                wav = wave
                yrange = [0, np.nanpercentile(flux[:, pixel_y, pixel_x], 99.9)]
                output['spec'] = [
                    dict(flux=npl(flx), error=npl(error), wave=npl(wav), yrange=npl(yrange))]
                output['status'] = "ok"
                output['message'] = ""
            else:
                output['spec'] = []
                output['status'] = "warning"
                output['message'] = "The point is out of the cube field-of-view."

        elif self.survey == 'atlas3d':
            file_cube = f"{settings.IFU_PATH}/atlas3d/{self.filename}.fits"
            file_cube = file_check(file_cube)
            scale = 0.8
            with fits.open(file_cube) as hdul:
                hdr = hdul[0].header
                flux = hdul[0].data
                err = np.sqrt(hdul[1].data)
                t = hdul[2].data
            wave = wave_hdr(hdr, index='1')

            pix_x = np.round(t['A'] / scale).astype(int)
            pix_y = np.round(t['D'] / scale).astype(int)
            nx = np.round(np.max(pix_x) - np.min(pix_x)+1).astype(int)
            ny = np.round(np.max(pix_y) - np.min(pix_y)+1).astype(int)
            sz = [ny, nx]
            imsk = np.full(sz, np.nan)
            # indexes = np.ravel_multi_index((pix_y, pix_x), [nx, ny])
            # img[indexes] = np.arange(len(pix_x))

            imsk[-np.min(pix_y) + pix_y,
                 -np.min(pix_x) + pix_x] = np.arange(len(pix_x))

            ind_center = np.argmin(np.linalg.norm([pix_x, pix_y], axis=0))
            w = WCS(naxis=2)

            w.wcs.crpix = [-np.min(pix_x) + pix_x[ind_center],
                           -np.min(pix_y) + pix_y[ind_center]]

            w.wcs.crval = [hdr['TCRVL6'], hdr['TCRVL7']]
            w.wcs.ctype = ['RA---TAN', 'DEC--TAN']
            w.wcs.cdelt = [-scale/3600.0, scale/3600.0]

            # fits.PrimaryHDU(data=img, header=w.to_header()).writeto(
            #     'tmp.fits', overwrite=True)
            ra, dec, arcsec_x, arcsec_y, pixel_x, pixel_y = \
                get_pointer_coords(w, sz, ra, dec, arcsec_x, arcsec_y)

            if (0 <= pixel_x < sz[0]) & (0 <= pixel_y < sz[1]):
                ind = imsk[pixel_x, pixel_y]
                if np.isfinite(ind):
                    ind = ind.astype(int)
                    flx = flux[ind, :]
                    error = err[ind, :]
                    wav = wave
                    yrange = [0, np.nanpercentile(flux[ind, :], 99.9)]
                    output['spec'] = [
                        dict(flux=npl(flx), error=npl(error), wave=npl(wav), yrange=npl(yrange))]
                    output['status'] = "ok"
                    output['message'] = ""
                else:
                    output['spec'] = []
                    output['status'] = "warning"
                    output['message'] = "The point is badpixel or out of coverage"
            else:
                output['spec'] = []
                output['status'] = "warning"
                output['message'] = "The point is out of the cube field-of-view"

        elif self.survey == 'bino':
            file_cube = f"{settings.IFU_PATH}/Binospec_IFU/{self.filename}.fits"
            file_cube = file_check(file_cube)

            with fits.open(file_cube) as hdul:
                hdr = hdul['IFU_CUBE'].header
                flux = hdul['IFU_CUBE'].data
                # err = hdul['STAT'].data

            # STAT extension contains weird values equal to flux
            err = np.full_like(flux, np.nan)

            wave = wave_hdr(hdr)

            w = WCS(hdr).dropaxis(-1)
            sz = w.pixel_shape

            ra, dec, arcsec_x, arcsec_y, pixel_x, pixel_y = \
                get_pointer_coords(w, sz, ra, dec, arcsec_x, arcsec_y)

            if (0 <= pixel_x < sz[0]) & (0 <= pixel_y < sz[1]):
                flx = flux[:, pixel_y, pixel_x]
                error = err[:, pixel_y, pixel_x]
                wav = wave
                yrange = [0, np.nanpercentile(flux[:, pixel_y, pixel_x], 99.9)]
                output['spec'] = [
                    dict(flux=npl(flx), error=npl(error), wave=npl(wav), yrange=npl(yrange))]
                output['status'] = "ok"
                output['message'] = ""
            else:
                output['spec'] = []
                output['status'] = "warning"
                output['message'] = "The point is out of the cube field-of-view."
        else:
            output['spec'] = []
            output['status'] = "error"
            output['message'] = f"Survey `{self.survey}` is not added to the IFU-Visualiser"
            pixel_x = None
            pixel_y = None

        output['ra'] = ra
        output['dec'] = dec
        output['arcsec_x'] = arcsec_x
        output['arcsec_y'] = arcsec_y
        output['pixel_x'] = pixel_x
        output['pixel_y'] = pixel_y

        return output
