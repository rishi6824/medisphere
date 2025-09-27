import json
import pandas as pd
from geopy.distance import geodesic
import os

def load_json_data(filename):
    """Load JSON data from file"""
    try:
        filepath = os.path.join('data', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_json_data(data, filename):
    """Save data to JSON file"""
    filepath = os.path.join('data', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in kilometers"""
    try:
        coords_1 = (lat1, lon1)
        coords_2 = (lat2, lon2)
        return geodesic(coords_1, coords_2).km
    except Exception as e:
        print(f"Error calculating distance: {e}")
        return float('inf')