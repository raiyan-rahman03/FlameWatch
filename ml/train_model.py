import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from tqdm import tqdm
import os

# Load the dataset
print("Loading dataset...")
dataset_path = r'C:\Users\User\Desktop\FlameWatch-main\FlameWatch-main\flame_watch_final_1.csv'
df = pd.read_csv(dataset_path)

# Print the dataset (first 5 rows)
print("Data loaded successfully:")
print(df.head())

# Check for any non-numeric columns and remove them
print("Removing non-numeric columns...")
df = df.select_dtypes(include=[np.number])

# Handling missing values: Fill NaN with the column mean
print("Filling missing values...")
df = df.fillna(df.mean())

# Separate features (X) and target (y)
print("Separating features and target...")
X = df.drop('is_fire', axis=1)  # Features (all columns except 'is_fire')
y = df['is_fire']               # Target (the 'is_fire' column)

# Split the data into training and testing sets (80% train, 20% test)
print("Splitting data into training and test sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Classifier
print("Initializing Random Forest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model with a progress bar
print("Starting model training with progress bar...")
for i in tqdm(range(100)):
    model.fit(X_train, y_train)

# Save the trained model
model_filename = r'C:\Users\User\Desktop\FlameWatch-main\FlameWatch-main\best_rf_model.pkl'
print(f"Saving the trained model as {model_filename}...")
joblib.dump(model, model_filename)
print(f"Model saved successfully at {model_filename}!")

# Test the model on the test data
print("Testing the model...")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy * 100:.2f}%")
