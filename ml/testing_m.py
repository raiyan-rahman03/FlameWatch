import pandas as pd
import joblib
import numpy as np
from sklearn.metrics import accuracy_score

# Load the original dataset
data_path = r'C:\Users\User\Desktop\FlameWatch-main\FlameWatch-main\flame_watch_final_1.csv'
data = pd.read_csv(data_path)

# Create a copy and modify it slightly
modified_data = data.copy()

# Introduce small random changes to some of the features (e.g., adding noise)
np.random.seed(42)  # For reproducibility
for column in modified_data.columns[:-1]:  # Exclude the target column
    noise = np.random.normal(0, 1.5, modified_data[column].shape)  # Change the noise level as needed
    modified_data[column] += noise

# Select features and target
features = modified_data.drop(columns=['is_fire'])  # Assuming 'is_fire' is the target column
target = modified_data['is_fire']

# Test with a small subset (e.g., first 10 rows)
X_test = features.head(10000)
y_test = target.head(10000)


# Load the saved model
model_path = r'C:\Users\User\Desktop\FlameWatch-main\FlameWatch-main\best_rf_model.pkl'
model = joblib.load(model_path)

# Make predictions
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

# Display predictions and accuracy
results = pd.DataFrame({
    'Actual': y_test,
    'Predicted': y_pred
})

print(f'Accuracy of the model on the modified test set: {accuracy * 100:.2f}%')
print("\nPredictions vs Actual:")
print(results)
