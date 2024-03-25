from django.db import models

# Create your models here.

# To be incorporated with a database like postgresql postgis TODO

# Comment on how you update a geospatial dataset when new data arrives. How would you handle conflicts or duplicate entries?

class Parcels(models.Model):
    id = models.CharField(primary_key=True, unique=True)
    proj_name = models.CharField(max_length=255)
    area = models.FloatField()
    status = models.CharField(max_length=255)
    area_sf = models.FloatField()
    building_f = models.FloatField()
    height_m = models.FloatField()
    storey = models.PositiveSmallIntegerField()
    gfa_sf = models.FloatField()
    density = models.FloatField()
    price = models.FloatField()
    units = models.PositiveSmallIntegerField()
    sold_per = models.FloatField()
    type = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    