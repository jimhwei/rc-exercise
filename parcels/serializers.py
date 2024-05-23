from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

class ParcelSerializer(serializers.Serializer):
    id = serializers.CharField(required=False, allow_null=True)
    area_sf = serializers.FloatField(required=False, allow_null=True)
    height_m = serializers.FloatField(required=False, allow_null=True)
    proj_name = serializers.CharField(required=False, allow_null=True)
    status = serializers.CharField(required=False, allow_null=True)
    height_m = serializers.FloatField(required=False, allow_null=True)
    parcel_type = serializers.CharField(required=False, allow_null=True)
    address = serializers.CharField(required=False, allow_null=True)
    geometry = GeometryField(required=False, allow_null=True)

class LocateParcelSerializer(serializers.Serializer):
    lat = serializers.FloatField(required=False, allow_null=True)
    lon = serializers.FloatField(required=False, allow_null=True)
    dist = serializers.FloatField(required=True, min_value=0.01)