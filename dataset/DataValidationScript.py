
import pandas as pd

# Load balanced dataset
df = pd.read_csv("dataset_35k_balance.csv")

print("Dataset Validation Report\n")

# 1. Dataset size
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

# 2. Check total size
if df.shape[0] == 35000:
    print("Dataset size is correct (35,000 records)")
else:
    print("Dataset size is incorrect")

# 3. Label distribution
print("\nLabel distribution:")
print(df["label"].value_counts())

counts = df["label"].value_counts()
if 0 in counts and 1 in counts and counts[0] == counts[1]:
    print("Dataset is balanced (50/50)")
else:
    print("Dataset is not balanced")

# 4. Missing values check
print("\nMissing values per column:")
print(df.isnull().sum())

if df.isnull().sum().sum() == 0:
    print("No missing values detected")
else:
    print("Missing values found")

# 5. Duplicate URLs check
duplicates = df.duplicated(subset=["url"]).sum()
print("\nNumber of duplicate URLs:", duplicates)

if duplicates == 0:
    print("No duplicate URLs found")
else:
    print("Duplicate URLs detected")

# 6. Statistical summary of features
print("\nStatistical summary of features:")
print(df.describe())

print("\nDataset is ready for model training if all checks above are valid")
