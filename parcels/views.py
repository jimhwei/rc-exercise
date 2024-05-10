# APIViews
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Parcel
from .serializers import ParcelSerializer
from django.contrib.gis.measure import D
from django.contrib.gis.geos import GEOSGeometry
from rest_framework.pagination import LimitOffsetPagination


class ParcelList(APIView):

    def get(self, request):
        parcels = Parcel.objects.all()
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(parcels, request)
        serializer = ParcelSerializer(result_page, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data) # This allows next and previous links


class ParcelFilter(APIView):

    def get(self, request):
        query_params = request.query_params
        serializer = ParcelSerializer(data=query_params)
        
        if not serializer.is_valid():
            # Return a 400 Bad Request with error messages if validation fails
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        filtered_parcels = Parcel.objects.all()
        
        if serializer.validated_data.get('area_sf'):
            filtered_parcels = filtered_parcels.filter(area_sf__gte=serializer.validated_data['area_sf'])
        
        if serializer.validated_data.get('height_m'):
            filtered_parcels = filtered_parcels.filter(height_m__gte=serializer.validated_data['height_m'])

        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(filtered_parcels, request)
        serializer = ParcelSerializer(result_page, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data) # This allows next and previous links

    
class LocateParcelById(APIView):
    
    # Can test with http://127.0.0.1:8000/parcels/locate/1?dist=10
    def get(self, request, id):
        filtered_parcel = Parcel.objects.filter(id=id).first()
        if not filtered_parcel:
            return Response("error: no record found", status=status.HTTP_404_NOT_FOUND)
        
        dist = request.GET.get('dist')
        if not dist:
            return Response("error: no distance entered", status=status.HTTP_400_BAD_REQUEST)
            
        reference_geom = filtered_parcel.geometry
        nearby_parcels = Parcel.objects.filter(
            geometry__distance_lte=(reference_geom, D(km=float(dist))))    
        serializer = ParcelSerializer(nearby_parcels, many=True)
        return Response(serializer.data)
    
    
class LocateParcelByCoordinates(APIView):
    
    # http://127.0.0.1:8000/parcels/locate/point?lat=43.64600&lon=-79.39613&dist=10
    def get(self, request):
        query_params = request.query_params
        serializer = ParcelSerializer(data=query_params)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        lat = serializer.validated_data["lat"]
        lon = serializer.validated_data["lon"]
        pnt = GEOSGeometry(f"POINT({lon} {lat})", srid=4326)
        dist = serializer.validated_data["dist"]
        
        nearby_parcels = Parcel.objects.filter(
            geometry__distance_lte=(pnt, D(km=dist))
            )
            
        serializer = ParcelSerializer(nearby_parcels, many=True)
        return Response(serializer.data)
    
# Notes:
# reference_geom:  SRID=4326;MULTIPOLYGON (((-79.40087676853099 43.64868440553216, -79.3999790463937 43.64886573351353, -79.39984676614499 43.64848821460149, -79.40073408421777 43.6483009414404, -79.40087676853099 43.64868440553216)))
# type of reference_geom:  <class 'django.contrib.gis.geos.collections.MultiPolygon'>

# pnt geom:  SRID=4326;POINT (-79.39613 43.646)
# type of pnt:  <class 'django.contrib.gis.geos.point.Point'>