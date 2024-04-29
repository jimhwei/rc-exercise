from django.db import models
from django.contrib.gis.db import models as gis_models


class Parcels(models.Model):
    # id = models.CharField(primary_key=True, unique=True, max_length=50)
    proj_name = models.CharField(max_length=255)
    # area = models.FloatField()
    status = models.CharField(max_length=255)
    # area_sf = models.FloatField()
    # building_f = models.FloatField()
    # height_m = models.FloatField()
    # storey = models.PositiveSmallIntegerField()
    # gfa_sf = models.FloatField()
    # density = models.FloatField()
    # price = models.FloatField()
    # units = models.PositiveSmallIntegerField()
    # sold_per = models.FloatField()
    # type = models.CharField(max_length=255)
    # address = models.CharField(max_length=255)
    geometry = gis_models.PolygonField(null=True)
    
    def __str__(self):
        return self.proj_name
    