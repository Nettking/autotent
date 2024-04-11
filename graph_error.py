import csv
import matplotlib.pyplot as plt
import numpy as np

def gather_data_from_csv(csv_filename="datalog.csv"):
    with open(csv_filename, "r") as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data

def plot_error_per_day(data):
    unique_days = sorted(set(row["Timestamp"] for row in data))
    day_to_index = {day: index for index, day in enumerate(unique_days)}

    # Initialize a dictionary to hold the aggregated errors for each day
    aggregated_errors = {day: [] for day in unique_days}
    
    for row in data:
        day = row["Timestamp"]
        error = abs(float(row["Error"]))
        aggregated_errors[day].append(error)

    # Aggregate errors for each day (e.g., by averaging)
    day_indices = [day_to_index[day] for day in unique_days]
    avg_errors = [np.mean(aggregated_errors[day]) for day in unique_days]

    # Plot the aggregated error values
    plt.plot(day_indices, avg_errors, label="Average Error")

    # Compute and plot the trend line for the aggregated data
    z = np.polyfit(day_indices, avg_errors, 1)
    p = np.poly1d(z)
    plt.plot(day_indices, p(day_indices), linestyle='--', label="Trend Line")

    # Determine the number of weeks and adjust tick frequency based on the total number of weeks
    total_weeks = (len(unique_days) + 6) // 7
    tick_spacing = 1 if total_weeks <= 10 else (2 if total_weeks <= 20 else (4 if total_weeks <= 40 else 8))
    week_ticks = range(0, total_weeks, tick_spacing)
    week_labels = [str(w) for w in week_ticks]

    # Apply the week number as x-axis ticks and increase font size
    plt.xticks(ticks=[w * 7 for w in week_ticks], labels=week_labels, fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(loc="upper left", fontsize=12)
    plt.xlabel("Week Number", fontsize=14)
    plt.ylabel("Average Error Value", fontsize=14)
    plt.title("Average Error per Week with Trend Line", fontsize=16)
    plt.show()

if __name__ == "__main__":
    data = gather_data_from_csv()
    plot_error_per_day(data)
