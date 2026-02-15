
import pandas as pd

# Load the final dataset with extracted features
df = pd.read_csv("dataset_features_15 (1).csv")

# Display dataset size
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

# Display column names
print("\nColumns in dataset:")
print(df.columns)

# Check for missing values
print("\nMissing values per column:")
print(df.isnull().sum())

# Display label distribution
print("\nLabel distribution:")
print(df["label"].value_counts())

# Preview first rows
print("\nPreview of first 5 rows:")
print(df.head())
