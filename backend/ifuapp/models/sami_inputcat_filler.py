from django.db import models


class SamiInputcatFiller(models.Model):
    """
    This group contains catalogue data derived from non-SAMI data

    Column description taken from https://datacentral.org.au/services/schema/#sami.
    """
    catid = models.BigIntegerField(primary_key=True, help_text="SAMI Galaxy ID")
    ra_obj = models.FloatField(blank=True, null=True, help_text="J2000 Right Ascension of object (deg)")
    dec_obj = models.FloatField(blank=True, null=True, help_text="J2000 Declination of object (deg)")
    z_spec = models.FloatField(blank=True, null=True, help_text="Spectroscopic redshift")
    fillflag = models.IntegerField(blank=True, null=True, help_text="Flag for different filler classes")

    class Meta:
        managed = False
        db_table = 'sami_inputcat_filler'
