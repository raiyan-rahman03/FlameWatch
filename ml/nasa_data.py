import pandas as pd
import requests
import random
from datetime import datetime, timedelta

# Load the CSV file containing latitude, longitude, and acquisition date
file_path = r"C:\Users\Md Raiyan\Desktop\nasa_data_fetch\SUOMI_VIIRS_C2_Global_7d.csv"
data = pd.read_csv(file_path)

# Filter to keep the first 500 unique entries of latitude and longitude
data_subset = data[['latitude', 'longitude', 'acq_date']].drop_duplicates(subset=['latitude', 'longitude'])

# If there are more than 500 entries, limit to the first 500
data_subset = data_subset.sample(n=2000, random_state=42) 

# Save the unique subset to a CSV file
subset_file_path = r"C:\Users\Md Raiyan\Desktop\nasa_data_fetch\nasa_subset_data.csv"
data_subset.to_csv(subset_file_path, index=False)
print(f"Unique subset saved as 'nasa_subset_data.csv'. Total rows: {data_subset.shape[0]}")

# Parameters for the NASA POWER API (daily parameters related to wildfire prediction)
parameters = "PW,PS,TOA_SW_DNI,T2M,T2M_MAX,T2M_MIN,RH2M,GWETROOT,QV10M,TOA_SW_DWN,QV2M,WS10M,WS10M_MAX,Z0M,GWETPROF,WS10M_MIN,SNODP,PRECTOTCORR"
community = "RE"

# Initialize a list to hold the results
results = []

# Number of random entries to select
num_random_entries = 200  # Change this to the number of random rows you want to select

# Randomly select the specified number of unique entries from the subset
random_entries = data_subset.sample(n=min(num_random_entries, data_subset.shape[0]), random_state=1)

# Loop over the filtered random data to fetch weather data from NASA POWER API
total_entries = random_entries.shape[0]
for iteration, (index, row) in enumerate(random_entries.iterrows(), start=1):
    latitude = row['latitude']
    longitude = row['longitude']
    acq_date = row['acq_date']

    # Convert acquisition date to datetime and adjust the date range
    acq_date_dt = datetime.strptime(acq_date, '%Y-%m-%d')
    
    # Print progress with iteration count
    print(f"Fetching data for entry {iteration}/{total_entries}: Latitude {latitude}, Longitude {longitude}, Index {index}")

    # Define the date range for the API request


    # Define the API request URL with the modified dates
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters={parameters}&community={community}&longitude={longitude}&latitude={latitude}&&start=20240518&end=20240520&format=JSON"

    # Make the request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        json_data = response.json()

        # Extract the data you want and store it in results
        if 'properties' in json_data and 'parameter' in json_data['properties']:
            daily_data = json_data['properties']['parameter']
            for date in daily_data['T2M']:
                results.append({
                    'latitude': latitude,
                    'longitude': longitude,
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
    else:
        print(f"Failed to fetch data for Latitude: {latitude}, Longitude: {longitude}, Status Code: {response.status_code}")

# Convert results to DataFrame and save as CSV
results_df = pd.DataFrame(results)
results_df.to_csv(r"C:\Users\Md Raiyan\Desktop\nasa_data_fetch\nasa_power_data_6.csv", index=False)

print("Weather data saved as 'nasa_power_data.csv'.")
