from django.db import models
from django.contrib.gis.db import models as gis_models


class Parcel(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=50)
    proj_name = models.CharField(max_length=255, null=True)
    area = models.FloatField(null=True)
    status = models.CharField(max_length=255, null=True)
    area_sf = models.FloatField(null=True)
    building_f = models.FloatField(null=True)
    height_m = models.FloatField(null=True)
    storey = models.PositiveSmallIntegerField(null=True)
    gfa_sf = models.FloatField(null=True)
    density = models.FloatField(null=True)
    price = models.FloatField(null=True)
    units = models.PositiveSmallIntegerField(null=True)
    sold_per = models.FloatField(null=True)
    type = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    geometry = gis_models.MultiPolygonField(null=True)
    
    def __str__(self):
        return self.proj_name
    