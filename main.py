import requests
import numpy as np
import tqdm

CENTER_LAT = 44.2706  # Lat of the center point
CENTER_LON = -71.3033  # Long of the center point
GRID_SIZE = 16 # Elevation grid size
SPACING = 100 # Spacing between  points in meters

OUTPUT_NAME = 'elevation_matrix.csv'

def get_elevation(latitude, longitude):
    """Fetch the elevation for a given latitude and longitude using Open-Meteo"""
    url = "https://api.open-meteo.com/v1/elevation"
    params = {
        "latitude": latitude,
        "longitude": longitude
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["elevation"][0]
    else:
        print(f"Failed to retrieve data for {latitude}, {longitude}. Status code: {response.status_code}")
        return None

def generate_elevation_matrix(CENTER_LAT, CENTER_LON, grid_size, spacing):
    """Generate a grid_sizexgrid_size elevation matrix with points spaced spacing meters apart"""
    R = 6371000  # Earth radius in meters

    # Convert m to degs for both latitude and longitude - Haversine formula
    lat_spacing = spacing / R * (180 / np.pi)  # Approximate degree change for 50 meters
    lon_spacing = lat_spacing / np.cos(np.radians(CENTER_LAT))  # Adjust longitude spacing based on latitude

    elevation_matrix = np.zeros((grid_size, grid_size))

    # Generate the matrix of elevation points
    for i in tqdm.tqdm(range(grid_size), desc="Rows", unit="row"):
        for j in range(grid_size):
            # print(f"Gathering data for index: {i}, {j}\n")
            lat = CENTER_LAT + (i - grid_size // 2) * lat_spacing
            lon = CENTER_LON + (j - grid_size // 2) * lon_spacing
            
            # Get elevation for the point
            elevation = get_elevation(lat, lon)
            if elevation is not None:
                elevation_matrix[i, j] = int(elevation)
            else:
                elevation_matrix[i, j] = np.nan  # If elevation is not available, set as NaN
    
    return elevation_matrix

# Generate the elevation matrix
elevation_matrix = generate_elevation_matrix(CENTER_LAT, CENTER_LON, GRID_SIZE, SPACING)

# Print the elevation matrix
print("16x16 Elevation Matrix (in meters):")
print(elevation_matrix)

np.savetxt(OUTPUT_NAME, elevation_matrix.astype(int), delimiter=",", fmt="%d")
print(f"Data saved to {OUTPUT_NAME}")