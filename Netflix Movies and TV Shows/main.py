import pandas as pd
import numpy as np

df = pd.read_csv("netflix_titles.csv")

print("Missing values before cleaning")
print(df.isna().sum())

columns_to_fill = ["director", "cast", "country", "rating", "duration"]

for column in columns_to_fill:
    df[column] = df[column].fillna("Unknown")

print("\nMissing values after filling")
print(df.isna().sum())

duplicate_count = df.duplicated().sum()
print("\nDuplicate rows:", duplicate_count)

df = df.drop_duplicates()

df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")

print("\nMissing values after date conversion")
print(df.isna().sum())

print("\nMovies and TV Shows")
print(df["type"].value_counts())

countries = df.loc[df["country"] != "Unknown", "country"]
country_counts = countries.str.split(", ").explode().str.strip().value_counts()

print("\nTop 10 countries")
print(country_counts.head(10))

titles_by_year = df["release_year"].value_counts()

print("\nTop 10 release years")
print(titles_by_year.head(10))

genre_counts = (
    df["listed_in"]
    .str.split(", ")
    .explode()
    .str.strip()
    .value_counts()
)

print("\nTop 10 genres")
print(genre_counts.head(10))

release_years = df["release_year"].to_numpy()

print("\nNumPy statistics for release years")
print("Mean:", np.mean(release_years))
print("Median:", np.median(release_years))
print("Standard Deviation:", np.std(release_years))
print("Percentiles:", np.percentile(release_years, [25, 50, 75]))

movie_duration_text = df.loc[df["type"] == "Movie", "duration"]
movie_minutes_text = movie_duration_text.str.replace("min", "", regex=False)
movie_minutes = pd.to_numeric(movie_minutes_text, errors="coerce")
movie_minutes = movie_minutes.dropna().astype(int)

print("\nNumPy statistics for movie duration")
print("Mean:", np.mean(movie_minutes))
print("Median:", np.median(movie_minutes))
print("Standard Deviation:", np.std(movie_minutes))
print("Percentiles:", np.percentile(movie_minutes, [25, 50, 75]))