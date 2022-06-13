import numpy as np
from django.db import models

from rest_framework import serializers, viewsets, pagination, response
from rest_flex_fields import FlexFieldsModelSerializer
from silk.profiling.profiler import silk_profile
import serpy

from ifuapp.pagination import EnhancedPageNumberPagination
from ifuapp.utils import npl


class AtlasMorphkin(models.Model):
    """
    Morphological and kinematical properties of Atlas3D galaxies.

    Table D1 from Krajnovic et al. (2011, MNRAS, 414, 2923) "The Atlas3D project -- II. Morphologies, kinemetric features and alignment between photometric and kinematic axes of early-type galaxies" paper.

    http://www-astro.physics.ox.ac.uk/atlas3d/tables/Krajnovic2011_Atlas3D_Paper2_TableD1.txt
    """
    atlas_name = models.OneToOneField('AtlasParam', models.DO_NOTHING, db_column='atlas_name', primary_key=True,
                                      related_name="atlas_morphkin", related_query_name="atlas_morphkin",
                                      help_text="Principal designation from LEDA, which is used as standard designation for Atlas3D project. ``Galaxy'' column in the original table.")
    pa_phot = models.FloatField(
        blank=True, null=True, help_text="Global photometric PA measured east of north and within 2.5–3 half-light radii [deg].")
    e_paphot = models.FloatField(
        blank=True, null=True, help_text="Photometric PA uncertainty [deg].")
    eps = models.FloatField(
        blank=True, null=True, help_text="Global ellipticity measured within 2.5–3 half-light radii.")
    e_eps = models.FloatField(blank=True, null=True,
                              help_text="Ellipticity uncertainty.")
    pa_kin = models.FloatField(
        blank=True, null=True, help_text="Global kinematic PA measured east of north at the receding part of the velocity map [deg].")
    e_pa_kin = models.FloatField(
        blank=True, null=True, help_text="Kinematic PA uncertainty [deg].")
    psi = models.FloatField(blank=True, null=True,
                            help_text="Kinematic misalignment angle [deg].")
    k51 = models.FloatField(
        blank=True, null=True, help_text="Luminosity-weighted average ratio of the harmonic terms k5/k1 obtained by KINEMETRY.")
    e_k51 = models.FloatField(blank=True, null=True,
                              help_text="k5/k1 uncertainty.")
    max_k1 = models.FloatField(
        blank=True, null=True, help_text="Maximal rotational velocity reached within the SAURON FoV [km/s].")
    morph = models.CharField(max_length=16, blank=True,
                             null=True, help_text="Morphological properties of galaxies – B: bar, R: ring, BR: bar and ring, S: shells, I: other interaction feature and U: unknown.")
    dust = models.CharField(max_length=16, blank=True, null=True,
                            help_text="Dust features – D: dusty disc, F: dusty filament, B: blue nucleus and BR: blue ring. Combinations of these are possible.")
    kin_struct = models.CharField(
        max_length=16, blank=True, null=True, help_text="Kinematic structure - NF: no feature on the map, 2M: double maxima on the radial velocity profile; KT: kinematic twist; KDC: kinematically distinct core; CRC: counter-rotating core; 2s: double peak on a sigma map; LV: low-level velocity (non-rotator).")
    kin_group = models.CharField(
        max_length=16, blank=True, null=True, help_text="Kinematic group – a: LV galaxies, b: NRR galaxies, c: KDC and CRC galaxies, d: 2σ peak galaxies, e: all other RR galaxies and f: unclassified galaxies.")
    # cube = models.ForeignKey('Cube', models.DO_NOTHING, blank=True, null=True,
    #                          related_name="atlas_morphkin", related_query_name="atlas_morphkin", help_text="")

    class Meta:
        managed = False
        db_table = 'atlas_morphkin'
