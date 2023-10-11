import pandas as pd
import matplotlib.pyplot as plt
import os

# Read the CSV file
data_folder = 'sensor_readings' + os.sep + 'multi_sensor'
data_path = os.path.join(data_folder, 'data.csv')
df = pd.read_csv(data_path, sep=";")

# Convert the "Timestamp" column to a datetime object
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')

# Inform the user of the available columns to plot
print("\nAvailable columns to plot:")
column_map = {
    '1': 'Temperature',
    '2': 'Humidity',
    '3': 'CO2',
    '4': 'Noise',
    '5': 'Pressure'
}
for key, value in column_map.items():
    print(f"{key}. {value}")

# Determine the available time ranges
min_date = df['Timestamp'].min()
max_date = df['Timestamp'].max()
available_ranges = {
    '1. 1 Hour': '1H',
    '2. 1 Day': '1D',
    '3. 1 Week': '7D',
    '4. 1 Month': '30D',
}

# Define time range options
time_ranges = {
    '1': '1H',
    '2': '1D',
    '3': '7D',
    '4': '30D',
}

# Prompt the user to select a column to plot
column_choice = input("Enter the number of the column you want to plot: ")
selected_column = column_map.get(column_choice)

if not selected_column:
    print("Invalid column choice. Please enter a valid number.")
    exit()

print("\nAvailable time ranges:")
for key, value in available_ranges.items():
    print(f"{key}. {value}")
    
time_range_choice = input("Enter the number of the time range you want to plot: ")
selected_time_range = time_ranges.get(time_range_choice)


if selected_time_range:
    
    if selected_column:
        
        if selected_time_range == '1H':
            unique_hours = df['Timestamp'].dt.strftime('%Y-%m-%d %H').unique()
            print("Available hours:")
            for i, hour in enumerate(unique_hours, start=1):
                print(f"{i}. {hour}")
            
            hour_choice = input("Enter the number of the hour you want to plot: ")

            try:
                selected_hour_index = int(hour_choice) - 1
                if 0 <= selected_hour_index < len(unique_hours):
                    selected_hour = unique_hours[selected_hour_index]

                    # Filter data for the selected hour
                    filtered_df = df[df['Timestamp'].dt.strftime('%Y-%m-%d %H') == selected_hour]

                    # Plot the selected data
                    plt.figure(figsize=(12, 6))
                    plt.plot(filtered_df['Timestamp'], filtered_df[selected_column])

                    # Customize the plot
                    plt.title(f'{selected_column} Over Time for {selected_hour}')
                    plt.xlabel('Timestamp')
                    plt.ylabel('Value')
                    plt.grid(True)

                    # Rotate x-axis labels for better readability (optional)
                    plt.xticks(rotation=45)

                    # Show the plot
                    plt.tight_layout()
                    plt.show()
                else:
                    print("Invalid hour choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        elif selected_time_range == '1D':
            # Display all available days for selection
            unique_dates = df['Timestamp'].dt.date.unique()
            print("Available days:")
            for i, date in enumerate(unique_dates, start=1):
                print(f"{i}. {date}")

            day_choice = input("Enter the number of the day you want to plot: ")

            try:
                selected_day_index = int(day_choice) - 1
                if 0 <= selected_day_index < len(unique_dates):
                    selected_day = unique_dates[selected_day_index]
                    
                    # Convert to datetime.date
                    selected_day = pd.to_datetime(selected_day).date()

                    # Filter data for the selected day
                    filtered_df = df[df['Timestamp'].dt.date == selected_day]

                    # Check filtered data
                    print("Found data for the following hours: ", filtered_df['Timestamp'].dt.hour.unique())

                    # Plot the selected data
                    plt.figure(figsize=(12, 6))
                    plt.plot(filtered_df['Timestamp'], filtered_df[selected_column])

                    # Customize the plot
                    plt.title(f'{selected_column} Over Time for {selected_day}')
                    plt.xlabel('Timestamp')
                    plt.ylabel('Value')
                    plt.grid(True)

                    # Rotate x-axis labels for better readability (optional)
                    plt.xticks(rotation=45)

                    # Show the plot
                    plt.tight_layout()
                    plt.show()
                else:
                    print("Invalid day choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")


        elif selected_time_range == '7D':
            # Display all available weeks for selection
            unique_weeks = df['Timestamp'].dt.strftime('%U-%Y').unique()
            print("Available weeks:")
            for i, week in enumerate(unique_weeks, start=1):
                print(f"{i}. {week}")

            week_choice = input("Enter the number of the week you want to plot: ")

            try:
                selected_week_index = int(week_choice) - 1
                if 0 <= selected_week_index < len(unique_weeks):
                    selected_week = unique_weeks[selected_week_index]
                    
                    # Filter data for the selected week
                    filtered_df = df[df['Timestamp'].dt.strftime('%U-%Y') == selected_week]

                    # Plot the selected data
                    plt.figure(figsize=(12, 6))
                    plt.plot(filtered_df['Timestamp'], filtered_df[selected_column])

                    # Customize the plot
                    plt.title(f'{selected_column} Over Time for {selected_week}')
                    plt.xlabel('Timestamp')
                    plt.ylabel('Value')
                    plt.grid(True)

                    # Rotate x-axis labels for better readability (optional)
                    plt.xticks(rotation=45)

                    # Show the plot
                    plt.tight_layout()
                    plt.show()
                else:
                    print("Invalid week choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        elif selected_time_range == '30D':
            # Display all available months for selection
            unique_months = df['Timestamp'].dt.strftime('%b-%Y').unique()
            print("Available months:")
            for i, month in enumerate(unique_months, start=1):
                print(f"{i}. {month}")

            month_choice = input("Enter the number of the month you want to plot: ")

            try:
                selected_month_index = int(month_choice) - 1
                if 0 <= selected_month_index < len(unique_months):
                    selected_month = unique_months[selected_month_index]
                    
                    # Filter data for the selected month
                    filtered_df = df[df['Timestamp'].dt.strftime('%b-%Y') == selected_month]

                    # Plot the selected data
                    plt.figure(figsize=(12, 6))
                    plt.plot(filtered_df['Timestamp'], filtered_df[selected_column])

                    # Customize the plot
                    plt.title(f'{selected_column} Over Time for {selected_month}')
                    plt.xlabel('Timestamp')
                    plt.ylabel('Value')
                    plt.grid(True)

                    # Rotate x-axis labels for better readability (optional)
                    plt.xticks(rotation=45)

                    # Show the plot
                    plt.tight_layout()
                    plt.show()
                else:
                    print("Invalid month choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        else:
            filtered_df = df
        
            # Plot the selected data
            plt.figure(figsize=(12, 6))
            plt.plot(filtered_df['Timestamp'], filtered_df[selected_column])

            # Customize the plot
            plt.title(f'{selected_column} Over Time')
            plt.xlabel('Timestamp')
            plt.ylabel('Value')
            plt.grid(True)

            # Rotate x-axis labels for better readability (optional)
            plt.xticks(rotation=45)

            # Show the plot
            plt.tight_layout()
            plt.show()
    else:
        print("Invalid data choice. Please enter a valid number.")
else:
    print("Invalid time range choice. Please enter a valid number.")
