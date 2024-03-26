from django.shortcuts import render
from django.http import JsonResponse
import json


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
        for key, value in criteria.items():
            if key in feature and feature[key] <= value:
                match = False
                break
        if match:
            filtered_features.append(feature)
    return filtered_features


def filter_parcels_by_features(request):
    
    # Note: The request payload should be flexible so that customers can have different filters.
    # I had planned to hard code each value to a value like below and assign default values    
    # area_sf = float(request.GET.get('area_sf', 1000))
    # height_m = float(request.GET.get('height_m', 100))
    # and so on...
    
    # But dictionary requires key value pairs to be added much easier
    expected_params = {
    'area_sf': float,
    'height_m': float,
    'density': float,
    # and so on
    }

    # Check for any unexpected values and return error.
    for param in request.GET.keys():
        if param not in expected_params:
            return JsonResponse({'error': f'Unexpected parameter: "{param}". Please check the parameters.'}, status=400)
    
    criteria = {}
    for param, expected_type in expected_params.items():
        param_value = request.GET.get(param)  # Fetches the parameter value if present, else None

        # Proceed only if the parameter was provided in the request
        if param_value is not None:
            try:
                # Attempt to convert parameter to the expected type and add to criteria
                criteria[param] = expected_type(param_value)
            except ValueError:
                # If conversion fails, return an error
                return JsonResponse({'error': f'Invalid format for parameter: {param}. Expected a {expected_type.__name__}.'}, status=400)

    print("Criteria:", criteria)

    # Validate dataset
    dataset = is_valid_geojson('/Users/jwei/Projects/ratio_django_api/ratio_city_toronto_example_dataset.geojson')
    
    # Our dataset is in a geojson format, easier to deal with if dataset was flat
    # Ideally we would use a spatial database and query them that way. 
    flat_dataset = flatten_features(dataset)
    output_data = filter_features(flat_dataset, criteria)
    
    
    return JsonResponse(output_data, safe=False)




# from django.contrib.gis.db.models.functions import Distance
# from django.contrib.gis.geos import fromstr

# from parcels.models import Parcels
# from geopy.distance import geodesic as GD

# def calculate_centroid(): 
        
#     # TODO remove hard coding of dataset?
#     dataset = is_valid_geojson('/Users/jwei/Projects/ratio_django_api/ratio_city_toronto_example_dataset.geojson')
#     flat_dataset = flatten_features(dataset)
    
#     for polygon in flat_dataset:
#         # Calculate the sum of each dimension
#         coords = polygon['geometry']['coordinates'][0][0]
        
#         sum_x = sum(coord[0] for coord in coords)
#         sum_y = sum(coord[1] for coord in coords)
        
#         # Calculate the mean of each dimension
#         mean_x = sum_x / len(coords)
#         mean_y = sum_y / len(coords)
        
#         polygon['centroid']=(mean_y, mean_x)
    
#     return flat_dataset


# def locate_nearby_parcels(request):
    
#     # Test if requests are empty, or invalid
    
#     # Tests if user tries to submit both id and geometry
#     # After receiving data
#         # Checks if using an id
#         # Or checks if using a geometry point from a "Map"

#     # Maybe using some kind of tool or third party library (geopy)
#         # find the centroid of all available properties
#         # use some kind of caluclation between xys between all centroids
    
#     q = calculate_centroid()
#     id = int(request.GET.get('id', 0)) #TODO assuming it is an int
#     lat,lon = q[id]['centroid']
#     # TODO we can't have both id and lat logn at once
#     if not id:
#         lat = float(request.GET.get('lat')) #43.64436663845263
#         lon = float(request.GET.get('lon')) #-79.39299031747248
#     distance_km = float(request.GET.get('distance', 1))  # Default to 1 km #TODO this is a string
#     # print(lat, lon, distance_km)
#     # print(type(lat), type(lon), type(distance_km))
    
#     selection =(lat, lon)
    
#     located_features = []
#     for shape in q:
#         if GD(selection, shape['centroid']).km < distance_km: # Geodesic distance
#             located_features.append(shape)
    
#     # point = fromstr(f'POINT({lon} {lat})', srid=4326)
#     # print(point)
#     # nearby_parcels = Parcels.objects.annotate(distance=Distance('geometry', point)).filter(distance__lte=distance_km)
#     # data = list(nearby_parcels.values('parcel_id', 'address', 'distance'))
#     return JsonResponse(located_features, safe=False)