from django.shortcuts import render
from django.http import JsonResponse
import json

# Following a YouTube tutorial... TODO Understand this??
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated


import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(message)s', filename='/Users/jwei/Projects/ratio_django_api/takehome/parcels/views.log', encoding='utf-8', level=logging.DEBUG)


# Create your views here.

# function to validate the incoming json with a standard template

def has_empty_values(d): 
    for value in d.values():
        if value == "" or value == None:
            logging.warning("Empty value") # TODO but for which key?
            return True
    return False

# Temporary until a database is implemented
def is_valid_geojson(filepath):     # TODO see security note regarding filepath...
    
    try: 
        
        with open(filepath) as f:
            data = json.load(f)
        
        for feature in data['features']:
            has_empty_values(feature["properties"])
                
        return data
    
    except Exception as e:
        logging.error(f"Exception occured: {e}")

    
    # TODO validates the data 
        # a.	Check for valid data, but you have to know what is valid data first
        # b.	Check if there will be error cases. E.g., strings, negative integers, is null, 0
        #     i.	If coordinate is invalid, then record is invalid
        # c.	Consider default value if necessary


def flatten_features(data):
    flattened = []
    for feature in data['features']:
        flat_feature = feature['properties']  # Assuming properties are already flat
        flat_feature['geometry'] = feature['geometry']  # Optionally add geometry or parts of it if needed
        flattened.append(flat_feature)
    return flattened


def filter_features(flattened_features, criteria):
    filtered_features = []
    for feature in flattened_features:
        match = True
        for key, (operation, value) in criteria.items():
            if key in feature:
                if operation == "greater_than" and not feature[key] > value:
                    match = False
                    break
                # TODO Add other operations as necessary
        if match:
            filtered_features.append(feature)
    return filtered_features

@api_view()
@permission_classes([AllowAny])
def filter_parcels_by_features(request):
    
    # Note: The request payload should be flexible so that customers can have different filters.
    area_sf = float(request.query_params['area_sf']) #TODO How to handle cases where no entry?
    height_m = float(request.query_params['height_m'])
    message = ("area_sf: " + str(area_sf), "height_m: " + str(height_m)) # Todo Debugging
    
    # The request is received and the parameters are extracted. 
    dataset = is_valid_geojson('/Users/jwei/Projects/ratio_django_api/ratio_city_toronto_example_dataset.geojson')
    
    flat_dataset = flatten_features(dataset)
    criteria = {
    'area': ('greater_than', area_sf),
    'height': ('greater_than', height_m),
    }

    output_data = filter_features(flat_dataset, criteria)
    
    
    # Test if requests are empty, or invalid
    # Filters data as needed based on one, two criteria, using a list comprehension perhaps
    
    # Return 
    
    return JsonResponse(output_data, safe=False)


def locate_nearby_parcels(request):
    
    # Test if requests are empty, or invalid
    
    # Tests if user tries to submit both id and geometry
    # After receiving data
        # Checks if using an id
        # Or checks if using a geometry point from a "Map"

    # Maybe using some kind of tool or third party library (geopy)
        # find the centroid of all available properties
        # use some kind of caluclation between xys between all centroids
        
    pass