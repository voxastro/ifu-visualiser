import numpy as np
from django.db import models
from ifuapp.utils import npl


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
    sami_catid = models.CharField(max_length=32, blank=True, null=True,
                                  help_text="'catid' identifier of SAMI survey target")
    sami_cube = models.CharField(max_length=32, blank=True, null=True,
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
    # cube = models.ForeignKey('Cube', models.DO_NOTHING, blank=True, null=True,
    #                          related_name="atlas_param", related_query_name="atlas_param", help_text="")

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
    # cube = models.ForeignKey('Cube', models.DO_NOTHING, blank=True, null=True,
    #                          related_name="atlas_morphkin", related_query_name="atlas_morphkin", help_text="")

    class Meta:
        managed = False
        db_table = 'atlas_morphkin'


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
