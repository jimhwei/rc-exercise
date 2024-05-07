from rest_framework import serializers
from .models import Parcel

class ParcelSerializer(serializers.Serializer):
    area_sf = serializers.FloatField(required=False, allow_null=True)
    height_m = serializers.FloatField(required=False, allow_null=True)