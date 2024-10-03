import requests
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

# Function to fetch data from NASA POWER API
def fetch_nasa_power_data(lat, lon, date):
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,TOA_SW_DNI,TOA_SW_DWN,PS,GWETROOT,QV10M,T2M_MAX,T2M_MIN,QV2M,SNODP,WS10M_MIN,WS10M_MAX,GWETPROF,Z0M,PW,PRECTOT,RH2M&community=RE&longitude={lon}&latitude={lat}&start={date}&end={date}&format=JSON"
    print("Fetching weather data from NASA POWER API...")
    response = requests.get(url)
    data = response.json()
    print("NASA POWER data fetched successfully.")
    return data['properties']['parameter']

# Function to preprocess the fetched data
def preprocess_nasa_power_data(lat, lon, date, data):
    print("Preprocessing NASA POWER data...")
    # Replace -999 values with 0
    processed_data = {}
    for param, value in data.items():
        processed_data[param] = [v if v != -999 else 0 for v in value.values()]

    # Convert to DataFrame
    df = pd.DataFrame(processed_data)
    
    # Add latitude, longitude, and date to match the training data
    df['latitude'] = lat
    df['longitude'] = lon
    df['date'] = date
    
    # Reorder columns to match training data
    column_order = ['latitude', 'longitude', 'date', 'T2M', 'T2M_MAX', 'T2M_MIN', 'RH2M', 'PW', 'PS', 'TOA_SW_DNI', 
                    'GWETROOT', 'QV10M', 'TOA_SW_DWN', 'QV2M', 'WS10M', 'WS10M_MAX', 'Z0M', 'GWETPROF', 
                    'WS10M_MIN', 'SNODP', 'PRECTOTCORR']
    
    df = df.reindex(columns=column_order)
    print("Preprocessing completed.")
    return df

# Function to load and test the model
def test_model(test_data):
    print("Loading the trained model...")
    model_path = r'FlameWatch\ml\best_model_tuned.pkl'
    model = joblib.load(model_path)
    
    print("Testing the model...")
    prediction = model.predict(test_data)
    prediction_prob = model.predict_proba(test_data)[:, 1]  # Probability of wildfire (class 1)
    
    return prediction, prediction_prob

# Main function
def main():
    # Get user inputs for location and date
    lat = float(input("Enter the latitude: "))
    lon = float(input("Enter the longitude: "))
    date = input("Enter the date (YYYYMMDD): ")

    # Fetch NASA POWER data
    nasa_data = fetch_nasa_power_data(lat, lon, date)

    # Preprocess the fetched data
    test_data = preprocess_nasa_power_data(lat, lon, date, nasa_data)

    # Test the model
    prediction, prediction_prob = test_model(test_data)
    
    # Print results
    print(f"Wildfire Prediction: {'Yes' if prediction[0] == 1 else 'No'}")
    print(f"Wildfire Probability: {prediction_prob[0] * 100:.2f}%")

if __name__ == "__main__":
    main()
