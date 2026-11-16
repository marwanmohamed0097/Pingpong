import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

train = pd.read_csv("train.csv")


print("\nData overview")
print(train.head())
print("Shape:", train.shape)
train.info()
print(train["count"].describe())


print("\nDuplicate rows")
duplicated_count = train.duplicated().sum()
print(duplicated_count)


print("\nPrepare datetime data")
train["datetime"] = pd.to_datetime(train["datetime"])
train["hour"] = train["datetime"].dt.hour
train["day_of_week"] = train["datetime"].dt.day_of_week
print(train[["datetime", "hour", "day_of_week", "count"]].head())


print("\nAverage rentals by hour")
average_by_hour = train.groupby("hour")["count"].mean()
print(average_by_hour)


print("\nAverage rentals by weather")
average_by_weather = train.groupby("weather")["count"].mean()
print(average_by_weather)

records_by_weather = train.groupby("weather")["count"].count()
print("Records per weather:")
print(records_by_weather)


print("\nAverage rentals by day of week")
average_by_day = train.groupby("day_of_week")["count"].mean()
print(average_by_day)


print("\nAverage rentals by working day")
average_by_workingday = train.groupby("workingday")["count"].mean()
print(average_by_workingday)


print("\nNumPy statistics for rentals")
count_values = train["count"].to_numpy()
print("Mean:", np.average(count_values))
print("Median:", np.median(count_values))
print("Standard deviation:", np.std(count_values))
print("Percentiles:", np.percentile(count_values, [25, 50, 75]))


print("\nTop 5 hours")
top_5_hours = average_by_hour.sort_values(ascending=False).head(5)
print(top_5_hours)


print("\nBottom 5 hours")
low_5_hours = average_by_hour.sort_values(ascending=True).head(5)
print(low_5_hours)


print("\nHours with average rentals above 300")
high_demand_hours = average_by_hour > 300
filtered_hours = average_by_hour[high_demand_hours]
print(filtered_hours)


average_by_hour.plot(kind="line", marker="o")
plt.title("Average bike rentals by hour")
plt.xlabel("Hour")
plt.ylabel("Average rentals")
plt.tight_layout()
plt.show()