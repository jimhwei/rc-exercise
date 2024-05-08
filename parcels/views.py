# APIViews
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Parcel
from .serializers import ParcelSerializer
from django.contrib.gis.measure import D
from django.contrib.gis.geos import GEOSGeometry


class ParcelList(APIView):

    def get(self, request):
        query_params = request.query_params
        serializer = ParcelSerializer(data=query_params)
        if serializer.is_valid(): 
            area_sf_value = serializer.validated_data["area_sf"]
            height_m_value = serializer.validated_data["height_m"]

        filtered_parcels = Parcel.objects.filter(area_sf__gte=area_sf_value).filter(height_m__gte=height_m_value)
        serializer = ParcelSerializer(filtered_parcels, many=True)
        return Response(serializer.data)

    
class LocateParcelById(APIView):
    
    # Can test with http://127.0.0.1:8000/LocateParcelsByCoordinates/?lat=43.64600&lon=-79.39613&dist=0.1
    def get(self, request):
        query_params = request.query_params
        serializer = ParcelSerializer(data=query_params)
        
        if serializer.is_valid(): 
            parcel_id = serializer.validated_data["id"]
            parcel = Parcel.objects.filter(id=parcel_id).first()
            dist = serializer.validated_data["dist"]
            
            reference_geom = parcel.geometry        
            nearby_parcels = Parcel.objects.filter(
            geometry__distance_lte=(reference_geom, D(km=dist)))    
            serializer = ParcelSerializer(nearby_parcels, many=True)
            return Response(serializer.data)
    
    
class LocateParcelByCoordinates(APIView):
    
    # can test with 43.64600, -79.39613
    def get(self, request):
        query_params = request.query_params
        serializer = ParcelSerializer(data=query_params)
        
        if serializer.is_valid(): 
            lat = serializer.validated_data["lat"]
            lon = serializer.validated_data["lon"]
            pnt = GEOSGeometry(f"POINT({lon} {lat})", srid=4326)
            dist = serializer.validated_data["dist"]
            
            nearby_parcels = Parcel.objects.filter(
                geometry__distance_lte=(pnt, D(km=dist))
            )
            
        serializer = ParcelSerializer(nearby_parcels, many=True)
        return Response(serializer.data)