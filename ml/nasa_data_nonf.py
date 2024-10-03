import pandas as pd
import requests
import random
from datetime import datetime, timedelta

# Load the wildfire occurrences dataset
wildfire_file_path = r"C:\Users\Md Raiyan\Desktop\nasa_data_fetch\nasa_power_data.csv"  # Your dataset with wildfire occurrences
wildfire_data = pd.read_csv(wildfire_file_path)

# Extract unique latitude and longitude from the wildfire data
fire_latitudes = wildfire_data['latitude'].unique()
fire_longitudes = wildfire_data['longitude'].unique()

# Define the geographical bounds for random sampling
lat_min = min(fire_latitudes) - 1  # Adjust as needed
lat_max = max(fire_latitudes) + 1  # Adjust as needed
lon_min = min(fire_longitudes) - 1  # Adjust as needed
lon_max = max(fire_longitudes) + 1  # Adjust as needed

# Function to check if the selected point is within the wildfire dataset
def is_point_safe(lat, lon):
    # Check if the latitude and longitude are not in the wildfire dataset
    return not any((wildfire_data['latitude'] == lat) & (wildfire_data['longitude'] == lon))

# Parameters for the NASA POWER API (daily parameters related to wildfire prediction)
parameters = "PW,PS,TOA_SW_DNI,T2M,T2M_MAX,T2M_MIN,RH2M,GWETROOT,QV10M,TOA_SW_DWN,QV2M,WS10M,WS10M_MAX,Z0M,GWETPROF,WS10M_MIN,SNODP,PRECTOTCORR"
community = "RE"

# Initialize a list to hold the results
non_fire_results = []

# Number of random non-fire entries to select
num_non_fire_entries = 1000  # Change this to the number of random rows you want to select

# Loop to generate non-fire locations
while len(non_fire_results) < num_non_fire_entries:
    # Generate random latitude and longitude
    random_lat = random.uniform(lat_min, lat_max)
    random_lon = random.uniform(lon_min, lon_max)

    # Check if this point is safe
    if is_point_safe(random_lat, random_lon):
        # Fetch weather data using the NASA POWER API
        url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters={parameters}&community={community}&longitude={random_lon}&latitude={random_lat}&start=20240518&end=20240520&format=JSON"

        # Make the request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            json_data = response.json()
            if 'properties' in json_data and 'parameter' in json_data['properties']:
                daily_data = json_data['properties']['parameter']
                for date in daily_data['T2M']:
                    non_fire_results.append({
                        'latitude': random_lat,
                        'longitude': random_lon,
                        'date': date,
                        'T2M': daily_data['T2M'][date],
                        'T2M_MAX': daily_data['T2M_MAX'][date],
                        'T2M_MIN': daily_data['T2M_MIN'][date],
                        'RH2M': daily_data['RH2M'][date],
                        'PW': daily_data['PW'][date],
                        'PS': daily_data['PS'][date],
                        'TOA_SW_DNI': daily_data['TOA_SW_DNI'][date],
                        'GWETROOT': daily_data['GWETROOT'][date],
                        'QV10M': daily_data['QV10M'][date],
                        'TOA_SW_DWN': daily_data['TOA_SW_DWN'][date],
                        'QV2M': daily_data['QV2M'][date],
                        'WS10M': daily_data['WS10M'][date],
                        'WS10M_MAX': daily_data['WS10M_MAX'][date],
                        'Z0M': daily_data['Z0M'][date],
                        'GWETPROF': daily_data['GWETPROF'][date],
                        'WS10M_MIN': daily_data['WS10M_MIN'][date],
                        'SNODP': daily_data['SNODP'][date],
                        'PRECTOTCORR': daily_data['PRECTOTCORR'][date],
                    })

        # Print progress
        print(f"Collected non-fire entry {len(non_fire_results)}/{num_non_fire_entries}: Latitude {random_lat}, Longitude {random_lon}")

# Convert results to DataFrame and save as CSV
non_fire_results_df = pd.DataFrame(non_fire_results)
non_fire_results_df.to_csv(r"C:\Users\Md Raiyan\Desktop\nasa_data_fetch\nasa_non_fire_data8.csv", index=False)

print("Non-fire data saved as 'nasa_non_fire_data.csv'.")
