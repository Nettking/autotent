import csv
import matplotlib.pyplot as plt

def gather_data_from_csv(csv_filename="sensor_readings/soil_moisture/data/datalog.csv"):
    with open(csv_filename, "r") as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data

def plot_error_per_day(data):
    sensors = set(row["SensorID"] for row in data)
    days = set(row["Timestamp"] for row in data)
    errors = {sensor: {day: 0 for day in days} for sensor in sensors}
    
    for row in data:
        day = row["Timestamp"]
        sensor = row["SensorID"]
        error = abs(float(row["Error"]))
        errors[sensor][day] = error

    for sensor, error_data in errors.items():
        days = sorted(error_data.keys())
        error_values = [error_data[day] for day in days]
        plt.plot(days, error_values, label=sensor)

    plt.legend(loc="upper left")
    plt.xlabel("Day")
    plt.ylabel("Error Value")
    plt.title("Error per Day for each Sensor")
    plt.show()

if __name__ == "__main__":
    data = gather_data_from_csv()
    plot_error_per_day(data)
