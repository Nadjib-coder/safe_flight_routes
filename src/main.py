# Main script to run the application

from src.data_fetcher import fetch_airplane_data, fetch_wildfire_data, fetch_volcanic_ash_data
from src.geospatial import is_in_dangerous_area
from src.pathfinding import find_safe_path

def main():
    wildfire_data = fetch_wildfire_data()
    volcanic_ash_data = fetch_volcanic_ash_data()
    
    airplane_data = fetch_airplane_data()
    start = (airplane_data['latitude'], airplane_data['longitude'])
    # goal = (desired_latitude, desired_longitude)
    
    # safe_path = find_safe_path(start, goal, wildfire_data, volcanic_ash_data)

if __name__ == "__main__":
    main()
