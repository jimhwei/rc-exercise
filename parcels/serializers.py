from rest_framework import serializers
from .models import Parcels

# Serialization helps convert Python Objects to JSON outputs
class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcels
        fields = ["id","proj_name","area","status","area_sf",
                  "building_f","height_m","storey","gfa_sf",
                  "density","price","sold_per","type","address",]