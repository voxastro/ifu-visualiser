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


class MangaDrp(models.Model):
    """
    Final summary table for the MaNGA Data Analysis Pipeline (DAP).

    Column description taken here https://data.sdss.org/datamodel/files/MANGA_SPECTRO_REDUX/DRPVER/drpall.html.
    """
    plate = models.IntegerField(blank=True, null=True, help_text="Plate ID")
    ifudsgn = models.IntegerField(
        blank=True, null=True, help_text="IFU Design ID (e.g. 12701)")
    plateifu = models.CharField(primary_key=True, max_length=11,
                                help_text="Plate+ifudesign name for this object (e.g. 7443-12701)")
    mangaid = models.CharField(max_length=11, blank=True, null=True,
                               help_text="MaNGA ID for this object (e.g. 1-114145)")
    versdrp2 = models.CharField(max_length=6, blank=True, null=True,
                                help_text="Version of mangadrp used for 2d reductions")
    versdrp3 = models.CharField(max_length=6, blank=True, null=True,
                                help_text="Version of mangadrp used for 3d reductions")
    verscore = models.CharField(max_length=6, blank=True, null=True,
                                help_text="Version of mangacore used for reductions")
    versutil = models.CharField(max_length=7, blank=True, null=True,
                                help_text="Version of idlutils used for reductions")
    versprim = models.CharField(max_length=4, blank=True, null=True,
                                help_text="Version of mangapreim used for reductions")
    platetyp = models.CharField(max_length=14, blank=True, null=True,
                                help_text="Plate type (e.g. MANGA, APOGEE-2&MANGA)")
    srvymode = models.CharField(max_length=12, blank=True, null=True,
                                help_text="Survey mode (e.g. MANGA dither, MANGA stare, APOGEE lead)")
    objra = models.FloatField(
        blank=True, null=True, help_text="Right ascension of the science object in J2000")
    objdec = models.FloatField(
        blank=True, null=True, help_text="Declination of the science object in J2000")
    ifuglon = models.FloatField(
        blank=True, null=True, help_text="Galactic longitude corresponding to IFURA/DEC")
    ifuglat = models.FloatField(
        blank=True, null=True, help_text="Galactic latitude corresponding to IFURA/DEC")
    ifura = models.FloatField(blank=True, null=True,
                              help_text="Right ascension of this IFU in J2000")
    ifudec = models.FloatField(
        blank=True, null=True, help_text="Declination of this IFU in J2000")
    ebvgal = models.FloatField(
        blank=True, null=True, help_text="E(B-V) value from SDSS dust routine for this IFUGLON, IFUGLAT")
    nexp = models.IntegerField(
        blank=True, null=True, help_text="Number of science exposures combined")
    exptime = models.FloatField(
        blank=True, null=True, help_text="Total exposure time")
    drp3qual = models.IntegerField(
        blank=True, null=True, help_text="Quality bitmask")
    bluesn2 = models.FloatField(
        blank=True, null=True, help_text="Total blue (S/N)^2 across all nexp exposures")
    redsn2 = models.FloatField(
        blank=True, null=True, help_text="Total red (S/N)^2 across all nexp exposures")
    harname = models.CharField(
        max_length=35, blank=True, null=True, help_text="IFU harness name")
    frlplug = models.IntegerField(
        blank=True, null=True, help_text="Frplug hardware code")
    cartid = models.CharField(
        max_length=30, blank=True, null=True, help_text="Cartridge ID number")
    designid = models.IntegerField(
        blank=True, null=True, help_text="Design ID number")
    cenra = models.FloatField(
        blank=True, null=True, help_text="Plate center right ascension in J2000")
    cendec = models.FloatField(
        blank=True, null=True, help_text="Plate center declination in J2000")
    airmsmin = models.FloatField(
        blank=True, null=True, help_text="Minimum airmass across all exposures")
    airmsmed = models.FloatField(
        blank=True, null=True, help_text="Median airmass across all exposures")
    airmsmax = models.FloatField(
        blank=True, null=True, help_text="Maximum airmass across all exposures")
    seemin = models.FloatField(
        blank=True, null=True, help_text="Best guider seeing")
    seemed = models.FloatField(
        blank=True, null=True, help_text="Median guider seeing")
    seemax = models.FloatField(
        blank=True, null=True, help_text="Worst guider seeing")
    transmin = models.FloatField(
        blank=True, null=True, help_text="Worst transparency")
    transmed = models.FloatField(
        blank=True, null=True, help_text="Median transparency")
    transmax = models.FloatField(
        blank=True, null=True, help_text="Best transparency")
    mjdmin = models.BigIntegerField(
        blank=True, null=True, help_text="Minimum MJD across all exposures")
    mjdmed = models.BigIntegerField(
        blank=True, null=True, help_text="Median MJD across all exposures")
    mjdmax = models.BigIntegerField(
        blank=True, null=True, help_text="Maximum MJD across all exposures")
    gfwhm = models.FloatField(blank=True, null=True,
                              help_text="Reconstructed FWHM in g-band")
    rfwhm = models.FloatField(blank=True, null=True,
                              help_text="Reconstructed FWHM in r-band")
    ifwhm = models.FloatField(blank=True, null=True,
                              help_text="Reconstructed FWHM in i-band")
    zfwhm = models.FloatField(blank=True, null=True,
                              help_text="Reconstructed FWHM in z-band")
    mngtarg1 = models.IntegerField(
        blank=True, null=True, help_text="Manga-target1 maskbit for galaxy target catalog")
    mngtarg2 = models.IntegerField(
        blank=True, null=True, help_text="Manga-target2 maskbit for galaxy target catalog")
    mngtarg3 = models.IntegerField(
        blank=True, null=True, help_text="Manga-target3 maskbit for galaxy target catalog")
    catidnum = models.IntegerField(
        blank=True, null=True, help_text="Primary target input catalog (leading digits of mangaid)")
    plttarg = models.CharField(
        max_length=30, blank=True, null=True, help_text="plateTarget reference file appropriate for this target")
    manga_tileid = models.IntegerField(
        blank=True, null=True, help_text="The ID of the tile to which this object has been allocated")
    nsa_iauname = models.CharField(
        max_length=19, blank=True, null=True, help_text="IAU-style designation based on RA/Dec (NSA)")
    ifudesignsize = models.IntegerField(
        blank=True, null=True, help_text="The allocated IFU size (0 = 'unallocated')")
    ifutargetsize = models.IntegerField(
        blank=True, null=True, help_text="The ideal IFU size for this object. The intended IFU size is equal to IFUTargetSize except if IFUTargetSize > 127 when it is 127, or < 19 when it is 19")
    ifudesignwrongsize = models.IntegerField(
        blank=True, null=True, help_text="The allocated IFU size if the intended IFU size was not available")
    z = models.FloatField(
        blank=True, null=True, help_text="The targeting redshift (identical to nsa_z for those targets in the NSA Catalog. For others, it is the redshift provided by the Ancillary programs)")
    zmin = models.FloatField(
        blank=True, null=True, help_text="The minimum redshift at which the galaxy could still have been included in the Primary sample")
    zmax = models.FloatField(
        blank=True, null=True, help_text="The maximum redshift at which the galaxy could still have been included in the Primary sample")
    szmin = models.FloatField(
        blank=True, null=True, help_text="The minimum redshift at which the galaxy could still have been included in the Secondary sample")
    szmax = models.FloatField(
        blank=True, null=True, help_text="The maximum redshift at which the galaxy could still have been included in the Secondary sample")
    ezmin = models.FloatField(
        blank=True, null=True, help_text="The minimum redshift at which the galaxy could still have been included in the Primary+ sample")
    ezmax = models.FloatField(
        blank=True, null=True, help_text="The maximum redshift at which the galaxy could still have been included in the Primary+ sample")
    probs = models.FloatField(
        blank=True, null=True, help_text="The probability that a Secondary sample galaxy is included after down-sampling. For galaxies not in the Secondary sample PROBS is set to the mean down-sampling probability")
    pweight = models.FloatField(
        blank=True, null=True, help_text="The volume weight for the Primary sample. Corrects the MaNGA selection to a volume limited sample.")
    psweight = models.FloatField(
        blank=True, null=True, help_text="The volume weight for the combined Primary and full Secondary samples. Corrects the MaNGA selection to a volume limited sample.")
    psrweight = models.FloatField(
        blank=True, null=True, help_text="The volume weight for the combined Primary and down-sampled Secondary samples. Corrects the MaNGA selection to a volume limited sample.")
    sweight = models.FloatField(
        blank=True, null=True, help_text="The volume weight for the full Secondary sample. Corrects the MaNGA selection to a volume limited sample.")
    srweight = models.FloatField(
        blank=True, null=True, help_text="The volume weight for the down-sampled Secondary sample. Corrects the MaNGA selection to a volume limited sample.")
    eweight = models.FloatField(
        blank=True, null=True, help_text="The volume weight for the Primary+ sample. Corrects the MaNGA selection to a volume limited sample.")
    esweight = models.FloatField(
        blank=True, null=True, help_text="The volume weight for the combined Primary+ and full Secondary samples. Corrects the MaNGA selection to a volume limited sample.")
    esrweight = models.FloatField(
        blank=True, null=True, help_text="The volume weight for the combined Primary+ and down-sampled Secondary samples. Corrects the MaNGA selection to a volume limited sample.")
    nsa_field = models.IntegerField(
        blank=True, null=True, help_text="SDSS field ID covering the target")
    nsa_run = models.IntegerField(
        blank=True, null=True, help_text="SDSS run ID covering the target")
    nsa_camcol = models.IntegerField(
        blank=True, null=True, help_text="SDSS camcol ID covering the catalog position")
    nsa_version = models.CharField(
        max_length=6, blank=True, null=True, help_text="Version of NSA catalogue used to select these targets")
    nsa_nsaid = models.IntegerField(
        blank=True, null=True, help_text="The NSAID field in the NSA catalogue referenced in nsa_version")
    nsa_nsaid_v1b = models.IntegerField(
        blank=True, null=True, help_text="The NSAID of the target in the NSA_v1b_0_0_v2 catalogue (if applicable).")
    nsa_z = models.FloatField(blank=True, null=True,
                              help_text="Heliocentric redshift")
    nsa_zdist = models.FloatField(
        blank=True, null=True, help_text="Distance estimate using peculiar velocity model of Willick et al. (1997); mulitply by c/Ho for Mpc")
    nsa_sersic_absmag_f = models.FloatField(
        blank=True, null=True, help_text="FUV absolute magnitude estimates in rest-frame bands from K-correction (Ωm=0.3, ΩΛ=0.7, h=1)")
    nsa_sersic_absmag_n = models.FloatField(
        blank=True, null=True, help_text="NUV absolute magnitude estimates in rest-frame bands from K-correction (Ωm=0.3, ΩΛ=0.7, h=1)")
    nsa_sersic_absmag_u = models.FloatField(
        blank=True, null=True, help_text="u absolute magnitude estimates in rest-frame bands from K-correction (Ωm=0.3, ΩΛ=0.7, h=1)")
    nsa_sersic_absmag_g = models.FloatField(
        blank=True, null=True, help_text="g absolute magnitude estimates in rest-frame bands from K-correction (Ωm=0.3, ΩΛ=0.7, h=1)")
    nsa_sersic_absmag_r = models.FloatField(
        blank=True, null=True, help_text="r absolute magnitude estimates in rest-frame bands from K-correction (Ωm=0.3, ΩΛ=0.7, h=1)")
    nsa_sersic_absmag_i = models.FloatField(
        blank=True, null=True, help_text="i absolute magnitude estimates in rest-frame bands from K-correction (Ωm=0.3, ΩΛ=0.7, h=1)")
    nsa_sersic_absmag_z = models.FloatField(
        blank=True, null=True, help_text="z absolute magnitude estimates in rest-frame bands from K-correction (Ωm=0.3, ΩΛ=0.7, h=1)")
    nsa_elpetro_absmag_f = models.FloatField(
        blank=True, null=True, help_text="FUV absolute magnitude in rest-frame bands, from elliptical Petrosian fluxes (Ωm=0.3, ΩΛ=0.7, h=1)")
    nsa_elpetro_absmag_n = models.FloatField(
        blank=True, null=True, help_text="NUV absolute magnitude in rest-frame bands, from elliptical Petrosian fluxes (Ωm=0.3, ΩΛ=0.7, h=1)")
    nsa_elpetro_absmag_u = models.FloatField(
        blank=True, null=True, help_text="u absolute magnitude in rest-frame bands, from elliptical Petrosian fluxes (Ωm=0.3, ΩΛ=0.7, h=1)")
    nsa_elpetro_absmag_g = models.FloatField(
        blank=True, null=True, help_text="g absolute magnitude in rest-frame bands, from elliptical Petrosian fluxes (Ωm=0.3, ΩΛ=0.7, h=1)")
    nsa_elpetro_absmag_r = models.FloatField(
        blank=True, null=True, help_text="r absolute magnitude in rest-frame bands, from elliptical Petrosian fluxes (Ωm=0.3, ΩΛ=0.7, h=1)")
    nsa_elpetro_absmag_i = models.FloatField(
        blank=True, null=True, help_text="i absolute magnitude in rest-frame bands, from elliptical Petrosian fluxes (Ωm=0.3, ΩΛ=0.7, h=1)")
    nsa_elpetro_absmag_z = models.FloatField(
        blank=True, null=True, help_text="z absolute magnitude in rest-frame bands, from elliptical Petrosian fluxes (Ωm=0.3, ΩΛ=0.7, h=1)")
    nsa_elpetro_amivar_f = models.FloatField(
        blank=True, null=True, help_text="FUV Inverse variance of nsa_elpetro_absmag in bands")
    nsa_elpetro_amivar_n = models.FloatField(
        blank=True, null=True, help_text="NUV Inverse variance of nsa_elpetro_absmag in bands")
    nsa_elpetro_amivar_u = models.FloatField(
        blank=True, null=True, help_text="u Inverse variance of nsa_elpetro_absmag in bands")
    nsa_elpetro_amivar_g = models.FloatField(
        blank=True, null=True, help_text="g Inverse variance of nsa_elpetro_absmag in bands")
    nsa_elpetro_amivar_r = models.FloatField(
        blank=True, null=True, help_text="r Inverse variance of nsa_elpetro_absmag in bands")
    nsa_elpetro_amivar_i = models.FloatField(
        blank=True, null=True, help_text="i Inverse variance of nsa_elpetro_absmag in bands")
    nsa_elpetro_amivar_z = models.FloatField(
        blank=True, null=True, help_text="z Inverse variance of nsa_elpetro_absmag in bands")
    nsa_sersic_mass = models.FloatField(
        blank=True, null=True, help_text="Stellar mass from K-correction fit (use with caution) for Sersic fluxes (Ωm=0.3, ΩΛ=0.7, h=1)")
    nsa_elpetro_mass = models.FloatField(
        blank=True, null=True, help_text="Stellar mass from K-correction fit (use with caution) for elliptical Petrosian fluxes (Ωm=0.3, ΩΛ=0.7, h=1)")
    nsa_elpetro_ba = models.FloatField(
        blank=True, null=True, help_text="Axis ratio used for elliptical apertures (for this version, same as ba90)")
    nsa_elpetro_phi = models.FloatField(
        blank=True, null=True, help_text="Position angle (east of north) used for elliptical apertures (for this version, same as ba90) [degrees]")
    nsa_extinction_f = models.FloatField(
        blank=True, null=True, help_text="FUV Galactic extinction from Schlegel, Finkbeiner, and Davis (1997), in bands")
    nsa_extinction_n = models.FloatField(
        blank=True, null=True, help_text="NUV Galactic extinction from Schlegel, Finkbeiner, and Davis (1997), in bands")
    nsa_extinction_u = models.FloatField(
        blank=True, null=True, help_text="u Galactic extinction from Schlegel, Finkbeiner, and Davis (1997), in bands")
    nsa_extinction_g = models.FloatField(
        blank=True, null=True, help_text="g Galactic extinction from Schlegel, Finkbeiner, and Davis (1997), in bands")
    nsa_extinction_r = models.FloatField(
        blank=True, null=True, help_text="r Galactic extinction from Schlegel, Finkbeiner, and Davis (1997), in bands")
    nsa_extinction_i = models.FloatField(
        blank=True, null=True, help_text="i Galactic extinction from Schlegel, Finkbeiner, and Davis (1997), in bands")
    nsa_extinction_z = models.FloatField(
        blank=True, null=True, help_text="z Galactic extinction from Schlegel, Finkbeiner, and Davis (1997), in bands")
    nsa_elpetro_th50_r = models.FloatField(
        blank=True, null=True, help_text="Elliptical Petrosian 50 percent light radius in SDSS r-band [arcsec]")
    nsa_petro_th50 = models.FloatField(
        blank=True, null=True, help_text="Azimuthally averaged SDSS-style Petrosian 50 percent light radius (derived from r band) [arcsec]")
    nsa_petro_flux_f = models.FloatField(
        blank=True, null=True, help_text="FUV Azimuthally-averaged SDSS-style Petrosian flux in bands (using r-band aperture) [nanomaggies]")
    nsa_petro_flux_n = models.FloatField(
        blank=True, null=True, help_text="NUV Azimuthally-averaged SDSS-style Petrosian flux in bands (using r-band aperture) [nanomaggies]")
    nsa_petro_flux_u = models.FloatField(
        blank=True, null=True, help_text="u Azimuthally-averaged SDSS-style Petrosian flux in bands (using r-band aperture) [nanomaggies]")
    nsa_petro_flux_g = models.FloatField(
        blank=True, null=True, help_text="g Azimuthally-averaged SDSS-style Petrosian flux in bands (using r-band aperture) [nanomaggies]")
    nsa_petro_flux_r = models.FloatField(
        blank=True, null=True, help_text="r Azimuthally-averaged SDSS-style Petrosian flux in bands (using r-band aperture) [nanomaggies]")
    nsa_petro_flux_i = models.FloatField(
        blank=True, null=True, help_text="i Azimuthally-averaged SDSS-style Petrosian flux in bands (using r-band aperture) [nanomaggies]")
    nsa_petro_flux_z = models.FloatField(
        blank=True, null=True, help_text="z Azimuthally-averaged SDSS-style Petrosian flux in bands (using r-band aperture) [nanomaggies]")
    nsa_petro_flux_ivar_f = models.FloatField(
        blank=True, null=True, help_text="FUV Inverse variance of nsa_petro_flux in bands [nanomaggies-2]")
    nsa_petro_flux_ivar_n = models.FloatField(
        blank=True, null=True, help_text="NUV Inverse variance of nsa_petro_flux in bands [nanomaggies-2]")
    nsa_petro_flux_ivar_u = models.FloatField(
        blank=True, null=True, help_text="u Inverse variance of nsa_petro_flux in bands [nanomaggies-2]")
    nsa_petro_flux_ivar_g = models.FloatField(
        blank=True, null=True, help_text="g Inverse variance of nsa_petro_flux in bands [nanomaggies-2]")
    nsa_petro_flux_ivar_r = models.FloatField(
        blank=True, null=True, help_text="r Inverse variance of nsa_petro_flux in bands [nanomaggies-2]")
    nsa_petro_flux_ivar_i = models.FloatField(
        blank=True, null=True, help_text="i Inverse variance of nsa_petro_flux in bands [nanomaggies-2]")
    nsa_petro_flux_ivar_z = models.FloatField(
        blank=True, null=True, help_text="z Inverse variance of nsa_petro_flux in bands [nanomaggies-2]")
    nsa_elpetro_flux_f = models.FloatField(
        blank=True, null=True, help_text="FUV Elliptical SDSS-style Petrosian flux in bands (using r-band aperture) [nanomaggies]")
    nsa_elpetro_flux_n = models.FloatField(
        blank=True, null=True, help_text="NUV Elliptical SDSS-style Petrosian flux in bands (using r-band aperture) [nanomaggies]")
    nsa_elpetro_flux_u = models.FloatField(
        blank=True, null=True, help_text="u Elliptical SDSS-style Petrosian flux in bands (using r-band aperture) [nanomaggies]")
    nsa_elpetro_flux_g = models.FloatField(
        blank=True, null=True, help_text="g Elliptical SDSS-style Petrosian flux in bands (using r-band aperture) [nanomaggies]")
    nsa_elpetro_flux_r = models.FloatField(
        blank=True, null=True, help_text="r Elliptical SDSS-style Petrosian flux in bands (using r-band aperture) [nanomaggies]")
    nsa_elpetro_flux_i = models.FloatField(
        blank=True, null=True, help_text="i Elliptical SDSS-style Petrosian flux in bands (using r-band aperture) [nanomaggies]")
    nsa_elpetro_flux_z = models.FloatField(
        blank=True, null=True, help_text="z Elliptical SDSS-style Petrosian flux in bands (using r-band aperture) [nanomaggies]")
    nsa_elpetro_flux_ivar_f = models.FloatField(
        blank=True, null=True, help_text="FUV Inverse variance of nsa_elpetro_flux in bands [nanomaggies-2]")
    nsa_elpetro_flux_ivar_n = models.FloatField(
        blank=True, null=True, help_text="NUV Inverse variance of nsa_elpetro_flux in bands [nanomaggies-2]")
    nsa_elpetro_flux_ivar_u = models.FloatField(
        blank=True, null=True, help_text="u Inverse variance of nsa_elpetro_flux in bands [nanomaggies-2]")
    nsa_elpetro_flux_ivar_g = models.FloatField(
        blank=True, null=True, help_text="g Inverse variance of nsa_elpetro_flux in bands [nanomaggies-2]")
    nsa_elpetro_flux_ivar_r = models.FloatField(
        blank=True, null=True, help_text="r Inverse variance of nsa_elpetro_flux in bands [nanomaggies-2]")
    nsa_elpetro_flux_ivar_i = models.FloatField(
        blank=True, null=True, help_text="i Inverse variance of nsa_elpetro_flux in bands [nanomaggies-2]")
    nsa_elpetro_flux_ivar_z = models.FloatField(
        blank=True, null=True, help_text="z Inverse variance of nsa_elpetro_flux in bands [nanomaggies-2]")
    nsa_sersic_ba = models.FloatField(
        blank=True, null=True, help_text="Axis ratio b/a from two-dimensional, single-component Sersic fit in r-band")
    nsa_sersic_n = models.FloatField(
        blank=True, null=True, help_text="Sersic index from two-dimensional, single-component Sersic fit in r-band")
    nsa_sersic_phi = models.FloatField(
        blank=True, null=True, help_text="Angle (E of N) of major axis in two-dimensional, single-component Sersic fit in r-band [degree]")
    nsa_sersic_th50 = models.FloatField(
        blank=True, null=True, help_text="50 percent light radius of two-dimensional, single-component Sersic fit to r-band")
    nsa_sersic_flux_f = models.FloatField(
        blank=True, null=True, help_text="FUV Two-dimensional, single-component Sersic fit flux in bands (fit using r-band structural parameters) [nanomaggies]")
    nsa_sersic_flux_n = models.FloatField(
        blank=True, null=True, help_text="NUV Two-dimensional, single-component Sersic fit flux in bands (fit using r-band structural parameters) [nanomaggies]")
    nsa_sersic_flux_u = models.FloatField(
        blank=True, null=True, help_text="u Two-dimensional, single-component Sersic fit flux in bands (fit using r-band structural parameters) [nanomaggies]")
    nsa_sersic_flux_g = models.FloatField(
        blank=True, null=True, help_text="g Two-dimensional, single-component Sersic fit flux in bands (fit using r-band structural parameters) [nanomaggies]")
    nsa_sersic_flux_r = models.FloatField(
        blank=True, null=True, help_text="r Two-dimensional, single-component Sersic fit flux in bands (fit using r-band structural parameters) [nanomaggies]")
    nsa_sersic_flux_i = models.FloatField(
        blank=True, null=True, help_text="i Two-dimensional, single-component Sersic fit flux in bands (fit using r-band structural parameters) [nanomaggies]")
    nsa_sersic_flux_z = models.FloatField(
        blank=True, null=True, help_text="z Two-dimensional, single-component Sersic fit flux in bands (fit using r-band structural parameters) [nanomaggies]")
    nsa_sersic_flux_ivar_f = models.FloatField(
        blank=True, null=True, help_text="FUV Inverse variance of nsa_sersic_flux in bands [nanomaggies-2]")
    nsa_sersic_flux_ivar_n = models.FloatField(
        blank=True, null=True, help_text="NUV Inverse variance of nsa_sersic_flux in bands [nanomaggies-2]")
    nsa_sersic_flux_ivar_u = models.FloatField(
        blank=True, null=True, help_text="u Inverse variance of nsa_sersic_flux in bands [nanomaggies-2]")
    nsa_sersic_flux_ivar_g = models.FloatField(
        blank=True, null=True, help_text="g Inverse variance of nsa_sersic_flux in bands [nanomaggies-2]")
    nsa_sersic_flux_ivar_r = models.FloatField(
        blank=True, null=True, help_text="r Inverse variance of nsa_sersic_flux in bands [nanomaggies-2]")
    nsa_sersic_flux_ivar_i = models.FloatField(
        blank=True, null=True, help_text="i Inverse variance of nsa_sersic_flux in bands [nanomaggies-2]")
    nsa_sersic_flux_ivar_z = models.FloatField(
        blank=True, null=True, help_text="z Inverse variance of nsa_sersic_flux in bands [nanomaggies-2]")

    class Meta:
        managed = False
        db_table = 'manga_drp'
