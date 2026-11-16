import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

train = pd.read_csv("train.csv")
print(train.head())

print(train.shape)
train.info()

print(train["count"].describe())

train["datetime"] = pd.to_datetime(train["datetime"])
train["hour"] = train["datetime"].dt.hour
print(train[["datetime", "hour", "count"]].head())
print(train["datetime"].dtype)

average_by_hour = train.groupby("hour")["count"].mean()
print(average_by_hour)

average_by_weather = train.groupby("weather")["count"].mean()
print(average_by_weather) #weather 4 has only one record, so its average is not representative

records_by_weather = train.groupby("weather")["count"].count()
print(records_by_weather) 

train["day_of_week"] = train["datetime"].dt.weekday
print(train[["datetime", "day_of_week"]].head())

average_by_day = train.groupby("day_of_week")["count"].mean()
print(average_by_day)

average_by_workingday = train.groupby("workingday")["count"].mean()
print(average_by_workingday)

print("####################")
duplicated_count = train.duplicated().sum()
print(duplicated_count)

count_values = train["count"].to_numpy()
print(np.average(count_values))
print(np.median(count_values))
print(np.std(count_values))
print(np.percentile(count_values, [25, 50, 75]))

top_5_hours = average_by_hour.sort_values(ascending=False).head(5)
print(top_5_hours)

low_5_hours = average_by_hour.sort_values(ascending=True).head(5)
print(low_5_hours)

high_demand_hours = average_by_hour > 300
print(high_demand_hours)

filtered_hours = average_by_hour[high_demand_hours]
print(filtered_hours)

average_by_hour.plot(kind="line",marker="o")
plt.title("Average bike rentals by hour")
plt.ylabel("Average rentals")
plt.show()