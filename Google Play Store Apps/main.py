import pandas as pd

df = pd.read_csv("googleplaystore.csv")

print(df.head())

print(df.shape)
df.info()

print(df.isna().sum())

df["Rating"] = df["Rating"].fillna(df["Rating"].median())

columns_to_fill = ["Type", "Content Rating", "Current Ver", "Android Ver"]

for column in columns_to_fill:
    df[column] = df[column].fillna("Unknown")

print(df.isna().sum())

duplicate_count = df.duplicated().sum()
print("Duplicate rows: ", duplicate_count)

df = df.drop_duplicates()

df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")
print(df["Reviews"].dtype)