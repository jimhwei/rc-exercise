from django.shortcuts import render
from django.http import JsonResponse
import json


# Create your views here.

# function to validate the incoming json with a standard template

# Temporary until a database is implemented
def return_valid_geojson(filepath):
    
    # TODO see security note regarding filepath...
    with open(filepath) as f:
        data = json.load(f)
    
    
    # validates the data 
        # a.	Check for valid data, but you have to know what is valid data first
        # b.	Check if there will be error cases. E.g., strings, negative integers, is null, 0
        #     i.	If coordinate is invalid, then record is invalid
        # c.	Consider default value if necessary


def filter_parcels_by_features(request): # What do i do with this request again? 
    
    # The request is received and the parameters are extracted. 
    # Note: The request payload should be flexible so that customers can have different filters. 
    
    # Test if requests are empty, or invalid
    # Filters data as needed based on one, two criteria, using a list comprehension perhaps
    
    # Return 
    pass
    
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