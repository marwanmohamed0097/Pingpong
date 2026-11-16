import pandas as pd
import numpy as np


df = pd.read_csv("googleplaystore.csv")

print("Dataset shape:", df.shape)

missing_before = df.isna().sum()
print("\nMissing values before cleaning:")
print(missing_before[missing_before > 0])


df["Rating"] = df["Rating"].fillna(df["Rating"].median())

columns_to_fill = ["Type", "Content Rating", "Current Ver", "Android Ver"]

for column in columns_to_fill:
    df[column] = df[column].fillna("Unknown")


duplicate_count = df.duplicated().sum()
print("\nDuplicate rows found:", duplicate_count)

df = df.drop_duplicates()


invalid_category = df["Category"].astype(str).eq("1.9")
print("Invalid rows removed:", invalid_category.sum())

df = df.loc[~invalid_category].copy()


df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")


size_mb = pd.to_numeric(
    df["Size"].str.replace("M", "", regex=False),
    errors="coerce"
)

size_kb = pd.to_numeric(
    df["Size"].str.replace("k", "", regex=False),
    errors="coerce"
) / 1024

df["Size_MB"] = size_mb.fillna(size_kb)


installs_text = df["Installs"].str.replace(",", "", regex=False)
installs_text = installs_text.str.replace("+", "", regex=False)

df["Installs_Number"] = pd.to_numeric(
    installs_text,
    errors="coerce"
)


price_text = df["Price"].str.replace("$", "", regex=False)
df["Price_USD"] = pd.to_numeric(price_text, errors="coerce")


missing_after = df.isna().sum()
print("\nMissing values after cleaning:")
print(missing_after[missing_after > 0])


apps_per_category = df["Category"].value_counts()

print("\nTop 10 categories by number of apps:")
print(apps_per_category.head(10))


rating_summary = df.groupby("Category")["Rating"].agg(["mean", "count"])
rating_summary = rating_summary.sort_values("mean", ascending=False)

print("\nTop 10 categories by average rating:")
print(rating_summary.head(10))


average_installs_by_category = (
    df.groupby("Category")["Installs_Number"]
    .mean()
    .sort_values(ascending=False)
)

print("\nTop 10 categories by average installs:")
print(average_installs_by_category.head(10))


ratings = df["Rating"].to_numpy()

print("\nNumPy statistics for ratings:")
print("Mean:", np.mean(ratings))
print("Median:", np.median(ratings))
print("Standard Deviation:", np.std(ratings))
print("Percentiles:", np.percentile(ratings, [25, 50, 75]))