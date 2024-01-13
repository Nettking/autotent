import requests
from datetime import datetime, timedelta

api_key = 'L2V332HTWSCPSNBSGY7EPYSDF'
api_key_2 = 'AM2VGQWMEQMCCLNLCYMYYFX6H'
location = 'halden'

def get_dates():
    # Define the start date as June 1st, 2023
    start_date = datetime(2023, 8, 1)

    # Get today's date
    end_date = datetime.now()

    # Generate a list of dates from start_date to end_date
    date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

    # Format and return the dates
    return date_list

def get_temp_every_hour(date):
    # Format the date for API request
    formatted_date = date.strftime('%Y-%m-%d')

    # Visual Crossing Weather API endpoint for hourly forecast within the date
    api_url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{formatted_date}/{formatted_date}?unitGroup=metric&include=hours&key={api_key}&contentType=json'
    
    # Make the API request
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        weather_data = response.json()

        # Extract and write hourly temperature to file
        hourly_temperature = weather_data['days'][0]['hours']
        with open('temperature_data.txt', 'a') as file:
            for hour in hourly_temperature:
                time = hour['datetime']
                temperature = hour['temp']
                file.write(f"{formatted_date} {time}: {temperature}\n")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Get the list of dates
date_list = get_dates()

# Get temperature for each date and write to file
for date in date_list:
    try:
        get_temp_every_hour(date)
        print(str(date) + ": Temperature collected")
    except:
        print(str(date) + ": Failed collection")