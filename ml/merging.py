import pandas as pd
import numpy as np

# File paths for the wildfire and non-wildfire datasets
wildfire_file_path = r"C:\Users\Md Raiyan\Desktop\nasa_data_fetch\nasa_merged_wildfire_data_1.csv"
non_wildfire_file_path = r"C:\Users\Md Raiyan\Desktop\nasa_data_fetch\non_wildfire_merged_data2.csv"

# Load the datasets
print("Loading wildfire dataset...")
wildfire_df = pd.read_csv(wildfire_file_path)

print("Loading non-wildfire dataset...")
non_wildfire_df = pd.read_csv(non_wildfire_file_path)

# Sample 3000 rows from each dataset
print("Sampling 3000 rows from wildfire dataset...")
wildfire_sample = wildfire_df.sample(n=3000, random_state=42)

print("Sampling 3000 rows from non-wildfire dataset...")
non_wildfire_sample = non_wildfire_df.sample(n=3000, random_state=42)

# Add the 'wild_fire_occurred' column
wildfire_sample['wild_fire_occurred'] = 1
non_wildfire_sample['wild_fire_occurred'] = 0

# Combine the samples into a single DataFrame
print("Merging the sampled datasets...")
combined_df = pd.concat([wildfire_sample, non_wildfire_sample], ignore_index=True)

# Shuffle the combined DataFrame
print("Shuffling the combined dataset...")
combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save the merged DataFrame to a new CSV file
output_file_path = r"C:\Users\Md Raiyan\Desktop\nasa_data_fetch\wildfire_final_dataset.csv"
print(f"Saving the combined dataset to {output_file_path}...")
combined_df.to_csv(output_file_path, index=False)

print("Combined dataset saved successfully!")
