
import pandas as pd

# Load dataset with extracted features
df = pd.read_csv("dataset_features_15.csv")

# Separate safe and malicious URLs
safe_df = df[df["label"] == 0]
mal_df = df[df["label"] == 1]

print("Number of safe URLs:", len(safe_df))
print("Number of malicious URLs:", len(mal_df))

# Randomly sample 17,500 from each class
safe_sample = safe_df.sample(n=17500, random_state=42)
mal_sample = mal_df.sample(n=17500, random_state=42)

# Combine both samples
final_35k = pd.concat([safe_sample, mal_sample])

# Shuffle dataset
final_35k = final_35k.sample(frac=1, random_state=42).reset_index(drop=True)

# Save final balanced dataset
final_35k.to_csv("dataset_35k_balanced.csv", index=False)

print("Balanced dataset created successfully")
print("Label distribution:")
print(final_35k["label"].value_counts())
print("Final dataset shape:", final_35k.shape)
