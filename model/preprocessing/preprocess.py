import pandas as pd

# 1. Load the original dataset
file_path = "dataset/Student Stress Factors.csv"

df = pd.read_csv(file_path)

print("Original dataset shape:", df.shape)

# 2. Remove the Timestamp column
df = df.drop(columns=["Timestamp"])

# 3. Remove duplicate rows
df = df.drop_duplicates()

# 4. Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# 5. Separate features and target
X = df.drop(columns=["How would you rate your stress levels?"])
y = df["How would you rate your stress levels?"]

print("\nFeatures:")
print(X.columns.tolist())

print("\nTarget:")
print(y.name)

print("\nTarget distribution:")
print(y.value_counts().sort_index())

print("\nFinal dataset shape:", df.shape)