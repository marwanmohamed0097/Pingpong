import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("StudentsPerformance.csv")

score_columns = ["math score", "reading score", "writing score"]

print("\n=== Average score for each subject ===")
print(df[score_columns].mean())

print("\n=== Average scores by gender ===")
gender_means = df.groupby("gender")[score_columns].mean()
print(gender_means)

print("\n=== Average scores by test preparation course ===")
prep_means = df.groupby("test preparation course")[score_columns].mean()
print(prep_means)

df["average_score"] = df[score_columns].mean(axis=1)

top_5 = df.sort_values("average_score", ascending=False).head(5)
bottom_5 = df.sort_values("average_score", ascending=True).head(5)

print("\n=== Top 5 records ===")
print(top_5[["average_score"] + score_columns])

print("\n=== Bottom 5 records ===")
print(bottom_5[["average_score"] + score_columns])

high_performers = df[df["average_score"] >= 90]

print("\n=== Records with an average score of 90 or higher ===")
print("Count:", len(high_performers))
print(high_performers[["average_score"] + score_columns].head())

for column in score_columns:
    scores = df[column]

    print(f"\n=== Statistics for {column} ===")
    print("Mean:", np.mean(scores))
    print("Median:", np.median(scores))
    print("Standard Deviation:", np.std(scores))
    print("Percentiles:", np.percentile(scores, [25, 50, 75]))

prep_means.plot(kind="bar")
plt.title("Average scores by test preparation course")
plt.xlabel("Test preparation course")
plt.ylabel("Average score")
plt.xticks(rotation=0)
plt.tight_layout()

gender_means.plot(kind="bar")
plt.title("Average scores by gender")
plt.xlabel("Gender")
plt.ylabel("Average score")
plt.xticks(rotation=0)
plt.tight_layout()

plt.show()