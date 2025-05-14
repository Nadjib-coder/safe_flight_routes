# Module for fetching data from APIs

import requests

# def fetch_airplane_data():
    
#     response = requests.get('')
#     response.raise_for_status()
#     return response.json()

def fetch_wildfire_data():
    # NASA FIRMS API endpoint example
    response = requests.get('https://firms.modaps.eosdis.nasa.gov/api/viirs?key=YOUR_API_KEY&bbox=-180,-90,180,90')
    response.raise_for_status()
    return response.json()

def fetch_volcanic_ash_data():
    # NOAA Volcanic Ash API endpoint example
    response = requests.get('https://www.volcano.si.edu/api/volcanic_ash?bbox=-180,-90,180,90')
    response.raise_for_status()
    return response.json()
