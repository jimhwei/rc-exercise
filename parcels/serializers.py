from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Parcel

class ParcelSerializer(serializers.Serializer):
    id = serializers.CharField(required=False, allow_null=True)
    area_sf = serializers.FloatField(required=False, allow_null=True)
    height_m = serializers.FloatField(required=False, allow_null=True)
    proj_name = serializers.CharField(required=False, allow_null=True)
    # area = serializers.FloatField(required=False, allow_null=True)
    status = serializers.CharField(required=False, allow_null=True)
    # building_f = serializers.FloatField(required=False, allow_null=True)
    height_m = serializers.FloatField(required=False, allow_null=True)
    # storey = serializers.FloatField(required=False, allow_null=True)
    # gfa_sf = serializers.FloatField(required=False, allow_null=True)
    # density = serializers.FloatField(required=False, allow_null=True)
    # price = serializers.FloatField(required=False, allow_null=True)
    # units = serializers.FloatField(required=False, allow_null=True)
    # sold_per = serializers.FloatField(required=False, allow_null=True)
    type = serializers.CharField(required=False, allow_null=True)
    address = serializers.CharField(required=False, allow_null=True)
    # geometry = serializers.GeometryField(required=False, allow_null=True) # ? https://www.django-rest-framework.org/api-guide/fields/#django-rest-framework-gis
    
class ParcelGeoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Parcel
        fields = ('id', 'area_sf', 'height_m', 'geometry')  # Include your geometry field
        geo_field = 'geometry'