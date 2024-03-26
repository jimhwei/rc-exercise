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
        for key, (operation, value) in criteria.items():
            if key in feature:
                if operation == "greater_than" and not feature[key] > value:
                    match = False
                    break
                # TODO Add other operations as necessary
        if match:
            filtered_features.append(feature)
    return filtered_features



def filter_parcels_by_features(request):
    
    # Note: The request payload should be flexible so that customers can have different filters.
    try:
        print(request.GET)
        # id = int(request.GET.get('id')) #TODO assuming it is an int
        # area = float(request.GET.get('area'))
        # area_sf = float(request.GET.get('area_sf'))
        # height_m = float(request.GET.get('height_m'))
        
        # Initialize a dictionary to hold validated parameters
        validated_params = {}
        
        expected_params = {
        'area': float,
        'area_sf': float,
        'height_m': float,
        'density': float,
        }
            
        for param, expected_type in expected_params.items():
            param_value = request.GET.get(param)
            if param_value is not None:
                try:
                    # Convert parameter to the expected type
                    validated_params[param] = expected_type(param_value)
                except ValueError:
                    # Return an error if the conversion fails
                    return JsonResponse({'error': f'Invalid format for parameter: {param}. Expected a {expected_type.__name__}.'}, status=400)

            print("Validated parameters:", validated_params)
        
    except ValueError:
        # TODO never gets executed because always a default value
        return JsonResponse({'error': 'Invalid parameters received. Recheck parameters'}, status=400)

    except TypeError:
        return JsonResponse({'error': 'Parameter not found, please check your parameter'}, status=400)

    
    # The request is received and the parameters are extracted. 
    dataset = is_valid_geojson('/Users/jwei/Projects/ratio_django_api/ratio_city_toronto_example_dataset.geojson')
    
    # flat_dataset = flatten_features(dataset)
    # criteria = {
    # 'area': ('greater_than', area_sf),
    # 'height': ('greater_than', height_m),
    # }

    # output_data = filter_features(flat_dataset, criteria)
    
    
    # # Test if requests are empty, or invalid
    # # Filters data as needed based on one, two criteria, using a list comprehension perhaps
    
    return JsonResponse(validated_params, safe=False)




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