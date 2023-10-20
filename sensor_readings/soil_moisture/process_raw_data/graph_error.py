import csv
import matplotlib.pyplot as plt

def gather_data_from_csv(csv_filename="sensor_readings/soil_moisture/data/datalog.csv"):
    with open(csv_filename, "r") as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data

def plot_error_per_day(data, selected_sensors):
    sensors = set(row["SensorID"] for row in data if row["SensorID"] in selected_sensors)
    days = set(row["Timestamp"] for row in data)
    errors = {sensor: {day: 0 for day in days} for sensor in sensors}
    
    for row in data:
        day = row["Timestamp"]
        sensor = row["SensorID"]
        error = abs(float(row["Error"]))
        if sensor in sensors:
            errors[sensor][day] = error

    num_sensors = len(sensors)
    fig, axs = plt.subplots(num_sensors, 1, figsize=(10, 4*num_sensors), sharex=True)
    
    if num_sensors == 1:
        axs = [axs]
    
    for idx, (sensor, error_data) in enumerate(sorted(errors.items())):
        days = sorted(error_data.keys())
        error_values = [error_data[day] for day in days]
        
        axs[idx].plot(days, error_values, color='blue')
        axs[idx].set_ylabel("Error Value")
        axs[idx].set_title(f"Sensor {sensor}")
        
    axs[-1].set_xlabel("Day")
    fig.suptitle("Error per Day for Selected Sensors", fontsize=16, y=1.02)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    data = gather_data_from_csv()
    
    print("Select a range of sensors to display:")
    print("1. A0-A2")
    print("2. A3-A6")
    print("3. A7-A9")
    choice = input("Enter your choice (1, 2, or 3): ")
    
    if choice == "1":
        selected_sensors = [f"A{i}" for i in range(3)]
    elif choice == "2":
        selected_sensors = [f"A{i}" for i in range(3, 7)]
    elif choice == "3":
        selected_sensors = [f"A{i}" for i in range(7, 10)]
    else:
        print("Invalid choice. Exiting.")
        exit()
    
    plot_error_per_day(data, selected_sensors)
