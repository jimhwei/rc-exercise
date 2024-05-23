from django.db import models
from django.contrib.gis.db import models as gis_models


class Parcel(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=50)
    proj_name = models.CharField(max_length=255, default='')
    area = models.FloatField(default=0)
    status = models.CharField(max_length=255, default='')
    area_sf = models.FloatField(default=0)
    building_f = models.FloatField(default=0)
    height_m = models.FloatField(default=0)
    storey = models.PositiveSmallIntegerField(default=0)
    gfa_sf = models.FloatField(default=0)
    density = models.FloatField(default=0)
    price = models.FloatField(default=0)
    units = models.PositiveSmallIntegerField(default=0)
    sold_per = models.FloatField(default=0)
    parcel_type = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    geometry = gis_models.MultiPolygonField(null=True) # Listed as Polygon, because that's the data type, what to do if there's bad geometry?
    
    def __str__(self):
        return self.proj_name
    