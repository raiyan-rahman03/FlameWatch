import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

# Load the trained model
model = joblib.load("C:/Users/Md Raiyan/Desktop/nasa_data_fetch/best_model_tuned.pkl")

# Load your non-wildfire dataset
non_wildfire_data_path = r"C:\Users\Md Raiyan\Desktop\nasa_data_fetch\non_wildfire_merged_data2.csv"  # Use raw string
non_wildfire_data = pd.read_csv(non_wildfire_data_path)

# Use the last 200 rows of the dataset
non_wildfire_data_last_200 = non_wildfire_data.tail(200)

# Preprocess the data as required
# Select the relevant features
features = non_wildfire_data_last_200[['latitude', 'longitude', 'T2M', 'T2M_MAX', 'T2M_MIN', 
                                         'RH2M', 'PW', 'PS', 'TOA_SW_DNI', 'GWETROOT', 
                                         'QV10M', 'TOA_SW_DWN', 'QV2M', 'WS10M', 
                                         'WS10M_MAX', 'Z0M', 'GWETPROF', 'WS10M_MIN', 
                                         'SNODP', 'PRECTOTCORR']]

# Replace -999 with 0 (if you need to do so)
features.replace(-999, 0, inplace=True)

# Ensure the model gets the right features in the correct order
# You can do this by creating a DataFrame with the same columns in the same order
# Example:
features = features.reindex(columns=model.feature_names_in_)

# Predict using the model
predictions = model.predict(features)
prediction_prob = model.predict_proba(features)[:, 1]  # Probability for the positive class

# Calculate accuracy, precision, recall, and F1-score
# Since this is a non-wildfire case, you can create a target variable with all zeros
true_labels = [0] * len(predictions)

# Calculate metrics
accuracy = accuracy_score(true_labels, predictions)
precision = precision_score(true_labels, predictions, zero_division=0)
recall = recall_score(true_labels, predictions, zero_division=0)
f1 = f1_score(true_labels, predictions, zero_division=0)

# Print the results
print("Predictions:", predictions)
print("Prediction Probabilities:", prediction_prob)
print(f"Accuracy: {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall: {recall * 100:.2f}%")
print(f"F1-Score: {f1 * 100:.2f}%")
