from django.db import models

class SamiGasKinPA(models.Model):
    """
    Gas Kinematic PA Catalogue

    Column description taken from https://datacentral.org.au/services/schema/#sami.
    """
    cubeid = models.CharField(blank=True, null=True, max_length=80, help_text="Internal unique cube ID")
    cubeidpub = models.CharField(primary_key=True, blank=True, null=True, max_length=15, help_text="Public unique cube ID for data release")
    cubename = models.CharField(blank=True, null=True, max_length=80, help_text="Internal unique cube name for blue cube")
    catid = models.BigIntegerField(help_text="SAMI Galaxy ID")
    pa_gaskin = models.FloatField(blank=True, null=True, help_text="Gas kinematic position angle. Anticlockwise, North=0 degrees (deg)")
    pa_gaskin_err = models.FloatField(blank=True, null=True, help_text="1-sigma error on the gas kinematic position angle (deg)")
    cube = models.ForeignKey('Cube', models.DO_NOTHING, db_column='cube', blank=True, null=True, related_name="sami_gaskin")

    class Meta:
        managed = False
        db_table = 'sami_gaskin'
