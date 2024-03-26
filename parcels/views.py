from django.http import JsonResponse
import json
from geopy.distance import geodesic as GD
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

# Tests if data is valid geojson
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
    """
    Filters a list of features based on specified criteria.
    """
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


def calculate_centroid(data): 
        
    flat_dataset = flatten_features(data)
    
    for polygon in flat_dataset:
        # Calculate the sum of each dimension
        coords = polygon['geometry']['coordinates'][0][0]
        
        sum_x = sum(coord[0] for coord in coords)
        sum_y = sum(coord[1] for coord in coords)
        
        # Calculate the mean of each dimension
        mean_x = sum_x / len(coords)
        mean_y = sum_y / len(coords)
        
        polygon['centroid']=(mean_y, mean_x)
    
    return flat_dataset


def locate_nearby_parcels(request):
    
    # TODO remove hard coding of dataset?
    dataset = is_valid_geojson('/Users/jwei/Projects/ratio_django_api/ratio_city_toronto_example_dataset.geojson')
    q = calculate_centroid(dataset)
    
    try:
        id = int(request.GET.get('id', 0))
        lat = float(request.GET.get('lat', None)) #43.64436663845263
        lon = float(request.GET.get('lon', None)) #-79.39299031747248
        distance_km = float(request.GET.get('dist', None))
    
    # Attempt to catch invalid parameters
    except ValueError:
        return JsonResponse({'error': 'Invalid parameter entered'}, status=400)
    except TypeError:
        return JsonResponse({'error': 'Invalid parameter entered'}, status=400)
    
    # Checks if user tries to submit both id and geometry
    if id and (lat or lon):
        return JsonResponse({'error': 'Please provide either an id or both latitude and longitude, not both.'}, status=400)
    elif not id and not (lat or lon):
        return JsonResponse({'error': 'Please provide either an id or both latitude and longitude.'}, status=400)
    if distance_km is None:
        return JsonResponse({'error': 'Please provide a distance parameter.'}, status=400)
    
    # Continue depending on input
    if id:
        q = calculate_centroid(dataset)
        selection = q[id]['centroid']
    
    else:
        selection =(float(lat), float(lon))
        
    located_features = []
    for shape in q:
        if GD(selection, shape['centroid']).km < float(distance_km): # Geodesic distance
            located_features.append(shape)
            
    return JsonResponse(located_features, safe=False)    