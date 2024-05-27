import json
import pytest
from .models import Parcel
from .serializers import ParcelSerializer
from django.urls import reverse
from rest_framework import status
from django.contrib.gis.geos import GEOSGeometry
from django.forms.models import model_to_dict


@pytest.fixture
def parcel_A(db) -> Parcel:
    geojson_dict={"type":"MultiPolygon","coordinates":[[[[-79.40087676853099,43.64868440553216],[-79.3999790463937,43.64886573351353],[-79.39984676614499,43.64848821460149],[-79.40073408421777,43.6483009414404],[-79.40087676853099,43.64868440553216]]]]}
    geojson_str = json.dumps(geojson_dict)
    geom = GEOSGeometry(geojson_str)
    return Parcel.objects.create(
        id='1', 
        area_sf=500, 
        height_m=10, 
        proj_name='Parcel A', 
        status='',
        parcel_type='',
        address='',
        area=0.0,
        building_f=0.0,
        density=0.0,
        gfa_sf=0.0,
        price=0.0,
        sold_per=0.0,
        storey=0.0,
        units=0.0,
        geometry=geom)

def parcel_converter(parcel):
    serializer = ParcelSerializer(parcel)
    converted_parcel = model_to_dict(parcel)
    print('parcel_conversion: ', converted_parcel['geometry'])
    print('serializer: ', serializer.data['geometry'])
    converted_parcel['geometry'] = serializer.data['geometry']
    return converted_parcel
    
def test_valid_parcel_serializer(db, parcel_A):
    '''Testing serializer/business logic '''
    serializer = ParcelSerializer(parcel_A)
    assert serializer.data == parcel_converter(parcel_A)

def test_parcel_filter(db, client, parcel_A):
    url = reverse('parcels-filter')
    response = client.get(url, {'area_sf': 500, 'height_m': 10})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'] == [parcel_converter(parcel_A)]
    assert len(response.data['results']) <= 10 # TODO should have exact objects, this line is not necessary

def test_locate_by_parcel_id(db, client, parcel_A):
    print("Parcel ID:", parcel_A.id)
    url = reverse('locate-parcels-by-id', kwargs={'id': parcel_A.id})
    # print("URL:", url)
    response = client.get(url, {'dist': 0.2}) 
    # print("Response: data", response.data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == [parcel_converter(parcel_A)]

def test_locate_by_coordinates(client, db, parcel_A):
    url = reverse('locate-parcels-by-coordinates')
    response = client.get(url, {'lat': 43.64600, 'lon': -79.39613, 'dist':10})
    print("Response:", response.data)
    assert response.status_code == status.HTTP_200_OK # TODO specify a response body that is expected
    assert response.data == [parcel_converter(parcel_A)]

def test_locate_by_coordinates_dist_error(client, db, parcel_A):
    url = reverse('locate-parcels-by-coordinates')
    response = client.get(url, {'lat': 43.64600, 'lon': -79.39613, 'dist':-1})
    print("Response:", response.data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# Old Below
# # from django.test import TestCase, Client

# # Create your tests here. TODO Update tests using Pytest

# class FilterParcelsByFeatureTests(TestCase):
    
#     def setUp(self):
#         self.client = Client()
        
#     def test_filter_by_single_criterion(self):
#         response = self.client.get('/filter/', {'area_sf': '1000'})
#         self.assertEqual(response.status_code, 200)
        
#     def test_filter_by_multiple_criteria(self):
#         response = self.client.get('/filter/', {'area_sf': '1000', 'height_m': '100'})
#         self.assertEqual(response.status_code, 200)

#     def test_unexpected_parameter(self):
#         response = self.client.get('/filter/', {'unexpected_param': '123'})
#         self.assertEqual(response.status_code, 400)

#     def test_invalid_parameter_format(self):
#         response = self.client.get('/filter/', {'height_m': 'not_a_number'})
#         self.assertEqual(response.status_code, 400)

# class LocateNearbyParcelsTests(TestCase):
    
#     def setUp(self):
#         self.client = Client()
    
#     def test_locate_by_parcel_id(self):
#         response = self.client.get('/locate/', {'id': '1', 'dist': '0.2'})
#         self.assertEqual(response.status_code, 200)

#     def test_locate_by_coordinates(self):
#         response = self.client.get('/locate/', {'lat': '43.644', 'lon': '-79.393', 'dist': '0.2'})
#         self.assertEqual(response.status_code, 200)

#     def test_invalid_parameters(self):
#         response = self.client.get('/locate/', {'lat': 'not_a_latitude', 'lon': 'not_a_longitude', 'dist': 'not_a_distance'})
#         self.assertEqual(response.status_code, 400)

#     def test_conflicting_parameters(self):
#         response = self.client.get('/locate/', {'id': '1', 'lat': '43.644', 'lon': '-79.393'})
#         self.assertEqual(response.status_code, 400)
