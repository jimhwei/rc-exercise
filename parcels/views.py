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

        # try:
        #     area_sf_value = serializer.validated_data["area_sf"]
        #     height_m_value = serializer.validated_data["height_m"]
            
        # except KeyError as e:
        #     return Response({"error" : f"Missing required parameter: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # filtered_parcels = Parcel.objects.filter(area_sf__gte=area_sf_value).filter(height_m__gte=height_m_value)
        # serializer = ParcelSerializer(filtered_parcels, many=True)
        # return Response(serializer.data)

    
class LocateParcelById(APIView):
    
    # Can test with http://127.0.0.1:8000/LocateParcelsByCoordinates/?lat=43.64600&lon=-79.39613&dist=0.1
    def get(self, request):
        query_params = request.query_params
        serializer = ParcelSerializer(data=query_params)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
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
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
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