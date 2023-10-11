import csv

def add_error_to_datalog(weeks_passed, day_number, csv_filename="datalog.csv"):
    # Define all possible sensors
    all_sensors = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9"]
    
    # Validate day number input
    if not (1 <= day_number <= 7):
        print("Invalid day number. It should be between 1 and 7.")
        return
    
    # Select sensors based on weeks passed
    sensors_this_week = all_sensors[:2 * weeks_passed]

    # Ask user for true humidity values of sensors introduced this day
    true_humidity_values = {}
    for sensor in sensors_this_week:
        true_value = float(input(f"Enter true humidity reading for sensor {sensor} on day {day_number}: "))
        true_humidity_values[sensor] = true_value

    # Read existing data
    with open(csv_filename, "r") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # Update data with error values for the specified day
    updated_data = []
    for row in data:
        sensor_id = row["SensorID"]
        # Only update sensors for which we have true values and that match the specified day
        if sensor_id in true_humidity_values and row["Timestamp"] == str(day_number):
            true_humidity = true_humidity_values[sensor_id]
            calculated_humidity = float(row["CalculatedHumidity"])
            error = calculated_humidity - true_humidity
            row["Error"] = error
        updated_data.append(row)

    # Write updated data back to CSV
    with open(csv_filename, "w", newline="") as f:
        fieldnames = ["ReadingID", "Timestamp", "SensorID", "RawReading", "CalculatedHumidity", "Error"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in updated_data:
            writer.writerow(row)

if __name__ == "__main__":
    weeks_passed = int(input("Enter the week number (1-5): "))
    day_number = int(input("Enter the day number (1-7): "))
    add_error_to_datalog(weeks_passed, day_number)
