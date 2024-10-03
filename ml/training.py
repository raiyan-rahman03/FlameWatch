import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
from tqdm import tqdm

# Load the dataset
print("Loading dataset...")
dataset_path = r'FlameWatch\ml\wildfire_final_dataset.csv'  # Your merged CSV file path
df = pd.read_csv(dataset_path)

# Print the dataset (first 5 rows)
print("Data loaded successfully:")
print(df.head())

# Remove non-numeric columns (if needed)
# df = df.select_dtypes(include=[np.number])

# Fill NaN values with the column mean
print("Filling missing values...")
df = df.fillna(df.mean())

# Separate features (X) and target (y)
print("Separating features and target...")
X = df.drop('wild_fire_occurred', axis=1)  # Features (all columns except 'wild_fire_occurred')
y = df['wild_fire_occurred']               # Target (the 'wild_fire_occurred' column)

# Split the data into training and testing sets (80% train, 20% test)
print("Splitting data into training and test sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the parameter grid for hyperparameter tuning
param_grid = {
    'n_estimators': [100, 300, 500],          # Number of trees
    'max_depth': [None, 10, 20, 30],          # Maximum depth of the tree
    'min_samples_split': [2, 5, 10],          # Minimum samples to split a node
    'min_samples_leaf': [1, 2, 4],            # Minimum samples in a leaf node
    'bootstrap': [True, False]                # Whether to bootstrap samples
}

# Initialize the Random Forest Classifier
print("Initializing Random Forest model...")
rf = RandomForestClassifier(n_jobs=4, random_state=42)

# Perform hyperparameter tuning using GridSearchCV
print("Starting hyperparameter tuning with GridSearchCV...")
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=4, verbose=2)

# Show a progress meter for training
grid_search.fit(X_train, y_train)

# Get the best model after hyperparameter tuning
best_model = grid_search.best_estimator_
print(f"Best Parameters: {grid_search.best_params_}")

# Save the best model
model_filename = r'C:\Users\Md Raiyan\Desktop\nasa_data_fetch\best_model_tuned.pkl'  # Update the path if necessary
print(f"Saving the best tuned model as {model_filename}...")
joblib.dump(best_model, model_filename)
print(f"Model saved successfully at {model_filename}!")

# Test the model on the test data
print("Testing the model...")
y_pred = best_model.predict(X_test)

# Show a progress bar while calculating metrics
print("Evaluating predictions...")
for _ in tqdm(range(len(y_pred)), desc="Predictions", unit="sample"):
    pass  # Progress simulation

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Print results
print(f"Accuracy: {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall: {recall * 100:.2f}%")
print(f"F1-Score: {f1 * 100:.2f}%")
