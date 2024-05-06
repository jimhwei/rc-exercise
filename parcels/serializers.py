from rest_framework import serializers
from .models import Parcel

# Serialization helps convert Python Objects to JSON outputs
class ParcelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Parcel
        # fields = ["proj_name", "status", 'geometry']
        
        fields = ["id","proj_name","status","geometry","address","area","area_sf",
                  "building_f","density","gfa_sf","height_m","price","sold_per","storey","type"
                  "units"]