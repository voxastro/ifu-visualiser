from django.db import models


class Cube(models.Model):
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
    cube = models.ForeignKey(Cube, models.DO_NOTHING, blank=True, null=True,
                             related_name="atlas_param", related_query_name="atlas_param", help_text="")

    class Meta:
        managed = False
        db_table = 'atlas_param'
