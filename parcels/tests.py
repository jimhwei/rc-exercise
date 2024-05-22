import pytest
from .models import Parcel
from .serializers import ParcelSerializer
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

@pytest.fixture
def parcel_A(db) -> Parcel:
    return Parcel.objects.create(proj_name='Parcel A', area_sf=500, height_m=10)

@pytest.fixture
def expected_parcel_data(parcel_A):
    return{
        'id': parcel_A.id, 
        'area_sf': parcel_A.area_sf, 
        'proj_name': parcel_A.proj_name, 
        'status': parcel_A.status, 
        'height_m': parcel_A.height_m, 
        'parcel_type': parcel_A.parcel_type, 
        'address': parcel_A.address, 
        'geometry': parcel_A.geometry, 
        'lat': None, 
        'lon': None, 
        'dist': None}

def test_parcel_filter(db, parcel_A, expected_parcel_data):
    client = APIClient()
    url = reverse('parcels-filter')
    response = client.get(url, {'area_sf': 500, 'height_m': 10})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'] == [expected_parcel_data]

    # assert len(response.data['results']) <= 10

def test_valid_parcel_serializer(db, parcel_A, expected_parcel_data):
    serializer = ParcelSerializer(parcel_A)
    assert serializer.data == expected_parcel_data


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
