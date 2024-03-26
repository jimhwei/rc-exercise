from django.http import JsonResponse
import json
from geopy.distance import geodesic as GD
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(message)s', 
                    filename='./views.log', encoding='utf-8', level=logging.DEBUG)


def has_empty_values(feat): 
    """Checks for empty or None values in a dictionary.

    Parameters:
        GeoJSON File in local directory.

    Returns:
        dict: The GeoJSON data if valid and no empty properties are found; otherwise, logs an error.
    """
    
    for key, value in feat.items():
        if value == "" or value is None:
            logging.warning(f"Empty value for key: {key}")
            return True
    return False


def is_valid_geojson(filepath):
    """Validates a GeoJSON file's properties for empty values.

    Parameters:
        GeoJSON File in local directory.

    Returns:
        dict: The GeoJSON data if valid and no empty properties are found; otherwise, logs an error.
    """
    
    try: 
        with open(filepath) as f:
            data = json.load(f)
        
        for feature in data['features']:
            has_empty_values(feature["properties"])
                
        return data
    
    except Exception as e:
        logging.error(f"Exception occured: {e}")
        return JsonResponse({'error': 'Invalid GeoJSON file'}, status=400)


def flatten_features(data):
    """
    Flattens a GeoJSON 'features' array into a list of features with geometry included.

    Parameters:
        data (dict): GeoJSON data containing a 'features' list.

    Returns:
        list: A list of flattened features, each including properties and geometry.
    """

    flattened = []
    for feature in data['features']:
        flat_feature = feature['properties']  # Assuming properties are already flat
        flat_feature['geometry'] = feature['geometry']  # Optionally add geometry or parts of it if needed
        flattened.append(flat_feature)
    return flattened


def filter_features(flattened_features, criteria):
    """
    Filters a list of flattened features based on specified criteria.

    Parameters:
        flattened_features (list): List of flattened features to filter.
        criteria (dict): A dictionary where each key-value pair represents a filter criterion. Currently
    only returns greater than criteria.

    Returns:
        list: A list of features that match all the specified criteria.
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
    """
    Processes a request to filter parcels based on features specified in the request parameters.

    Parameters:
        request (HttpRequest): The request object containing GET parameters for filtering.

    Returns:
        JsonResponse: A JSON response containing either the filtered dataset or an error message.
    """
    
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
    # and so on...
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


    # Validate dataset
    dataset = is_valid_geojson('./ratio_city_toronto_example_dataset.geojson')
    
    # Our dataset is in a geojson format, easier to deal with if dataset was flat
    # Ideally we would use a spatial database and query them that way. 
    flat_dataset = flatten_features(dataset)
    logging.debug("Criteria: "+ str(criteria))
    output_data = filter_features(flat_dataset, criteria)
    
    
    return JsonResponse(output_data, safe=False)


def calculate_centroid(data): 
    """
    Calculates the centroid for each polygon feature in a flattened dataset.
    The function calculates the centroid of each polygon by averaging the coordinates of 
    its vertices. Adds the centroid as a new key-value pair to each feature's dictionary.

    Parameters:
        data (dict): Flattened geojson format.

    Returns:
        list: A list of flattened features with an added 'centroid' key for each, representing
    the centroid's coordinates.
    """
        
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
    """
    Identifies and returns parcels within a specified distance from a given point or parcel ID.
    It returns nearby parcels based on the geodesic distance from the specified point or the centroid of
    the parcel associated with the given ID.

    Parameters:
        request (HttpRequest): The request object containing GET parameters for 'id', 'lat', 'lon', and 'dist'.

    Returns:
        JsonResponse: A JSON response containing a list of nearby parcels if successful; otherwise, returns
    an error JSON with a specific error message. 
    """
    
    logging.debug('Locate Nearby Parcels')
    
    dataset = is_valid_geojson('./ratio_city_toronto_example_dataset.geojson')
    q = calculate_centroid(dataset)
    
    try:
        id = int(request.GET.get('id', 0))
        lat = request.GET.get('lat', None) # 43.644
        lon = request.GET.get('lon', None) # -79.393
        distance_km = float(request.GET.get('dist', None))

        req_msg = "paramaters: id: " + str(id) + ", lat: " + str(lat) + ", lon: " + str(lon) + ", distance_km: " + str(distance_km)
        logging.debug(req_msg)

    
    # Attempt to catch invalid parameters
    except ValueError:
        return JsonResponse({'ValueError': 'Invalid parameter entered'}, status=400)
    except TypeError:
        return JsonResponse({'TypeError': 'Invalid parameter entered'}, status=400)
    
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
    
    # Checks compare centroid of all records and compares it with distance parameter
    located_features = []
    for shape in q:
        if GD(selection, shape['centroid']).km < float(distance_km): # Geodesic distance
            located_features.append(shape)
            
    return JsonResponse(located_features, safe=False)