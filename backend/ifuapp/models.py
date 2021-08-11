import numpy as np
from django.db import models
from ifuapp.utils import npl
from djangoql.queryset import DjangoQLQuerySet


class Cube(models.Model):
    """
    Spectral cubes model.
    """
    cube_id = models.IntegerField(primary_key=True)
    ra = models.FloatField(blank=True, null=True)
    dec = models.FloatField(blank=True, null=True)
    survey = models.CharField(max_length=32, blank=True, null=True)
    filename = models.CharField(max_length=64, blank=True, null=True)
    exptime = models.FloatField(blank=True, null=True)
    manga_id = models.CharField(max_length=32, blank=True, null=True)
    manga_plateifu = models.CharField(max_length=32, blank=True, null=True)
    sami_catid = models.CharField(max_length=32, blank=True, null=True)
    sami_cube = models.CharField(max_length=32, blank=True, null=True)
    califa_id = models.IntegerField(blank=True, null=True)
    califa_name = models.CharField(max_length=32, blank=True, null=True)
    califa_cube = models.CharField(max_length=32, blank=True, null=True)
    atlas_name = models.CharField(max_length=32, blank=True, null=True)

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

    objects = DjangoQLQuerySet.as_manager()


class AtlasParam(models.Model):
    """
    General parameters of the Atlas3D sample of 260 early-type (E and S0) galaxies

    Table 3 from Cappellari et. al (2011a, MNRAS, 413, 813) ``The Atlas3D project -- I. A volume-limited sample of 260 nearby early-type galaxies: science goals and selection criteria''
    http://www-astro.physics.ox.ac.uk/atlas3d/tables/Cappellari2011a_Atlas3D_Paper1_Table3.txt

    A slightly shortened field descriptions are taken from the notes to Table 3.
    """
    atlas_name = models.CharField(primary_key=True, max_length=32,
                                  help_text="Principal designation from LEDA, which is used as standard designation for Atlas3D project. ``Galaxy'' column in the original table.")
    ra = models.FloatField(blank=True, null=True,
                           help_text="Right Accession J2000 [deg.]")
    dec = models.FloatField(blank=True, null=True,
                            help_text="Declination J200 [deg.]")
    sbf = models.IntegerField(
        blank=True, null=True, help_text="SBF = 1 if the galaxy is in Tonry et al. (2001) and SBF = 2 if it is in Mei et al. (2007) or both.")
    nedd = models.IntegerField(
        blank=True, null=True, help_text="Number of redshift-independent distance determinations listed in the NED-D catalogue, excluding the ones based on kinematical scaling relations")
    virgo = models.BooleanField(
        blank=True, null=True, help_text="Virgo = 1 if the galaxies is contained within a sphere of radius R=3.5 Mpc from the centre of the cluster assumed at coordinates RA = 12h28m19s and Dec. = +12d40m (Mould et al. 2000) and distance D=16.5 Mpc (Mei et al. 2007)")
    vhel = models.FloatField(
        blank=True, null=True, help_text="Heliocentric velocity measured from the SAURON integral field stellar kinematics (1sigma error Vhel = 5 km/s) [km/s]")
    d = models.FloatField(blank=True, null=True, help_text="Distance [Mpc]")
    m_k = models.FloatField(
        blank=True, null=True, help_text="Total galaxy absolute magnitude in K-band [mag]")
    a_b = models.FloatField(
        blank=True, null=True, help_text="B-band foreground galactic extinction from Schlegel, Finkbeiner & Davis (1998) [mag]")
    type = models.FloatField(
        blank=True, null=True, help_text="Morphological T type from HyperLeda. E: T <= −3.5; S0: −3.5 < T <= −0.5")
    logre = models.FloatField(
        blank=True, null=True, help_text="Logarithm of projected half-light effective radius [arcsec]")
    cube = models.ForeignKey('Cube', models.DO_NOTHING, blank=True, null=True,
                             related_name="atlas_param", related_query_name="atlas_param", help_text="")

    class Meta:
        managed = False
        db_table = 'atlas_param'


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
    cube = models.ForeignKey('Cube', models.DO_NOTHING, blank=True, null=True,
                             related_name="atlas_morphkin", related_query_name="atlas_morphkin", help_text="")

    class Meta:
        managed = False
        db_table = 'atlas_morphkin'
