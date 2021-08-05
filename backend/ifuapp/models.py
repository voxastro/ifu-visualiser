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
    sami_catid = models.BigIntegerField(blank=True, null=True)
    sami_cube = models.CharField(max_length=32, blank=True, null=True)
    califa_id = models.IntegerField(blank=True, null=True)
    califa_name = models.CharField(max_length=32, blank=True, null=True)
    califa_cube = models.CharField(max_length=32, blank=True, null=True)
    atlas_name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cube'


class AtlasSample(models.Model):
    atlas_name = models.CharField(primary_key=True, max_length=32)
    ra = models.FloatField(blank=True, null=True)
    dec = models.FloatField(blank=True, null=True)
    sbf = models.IntegerField(blank=True, null=True)
    nedd = models.IntegerField(blank=True, null=True)
    virgo = models.BooleanField(blank=True, null=True)
    vhel = models.FloatField(blank=True, null=True)
    d = models.FloatField(blank=True, null=True)
    m_k = models.FloatField(blank=True, null=True)
    a_b = models.FloatField(blank=True, null=True)
    type = models.FloatField(blank=True, null=True)
    logre = models.FloatField(blank=True, null=True)
    cube = models.ForeignKey(Cube, models.DO_NOTHING, blank=True, null=True,
                             related_name="atlas_sample", related_query_name="atlas_sample",)

    class Meta:
        managed = False
        db_table = 'atlas_sample'
