from django.db import models

# Create your models here.

# To be incorporated with a database like postgresql postgis

# Comment on how you update a geospatial dataset when new data arrives. How would you handle conflicts or duplicate entries?

class Parcels(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True, unique=True)
    proj_name = models.CharField(max_length=255)
    area = models.DecimalField(decimal_places=2)
    status = models.CharField(max_length=255)
    area_sf = models.DecimalField(decimal_places=2)
    building_f = models.DecimalField(decimal_places=2)
    height_m = models.DecimalField(decimal_places=2)
    storey = models.PositiveSmallIntegerField()
    gfa_sf = models.DecimalField(decimal_places=2)
    density = models.DecimalField(decimal_places=2)
    price = models.DecimalField(decimal_places=2)
    units = models.PositiveSmallIntegerField()
    sold_per = models.DecimalField(decimal_places=2)
    type = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    