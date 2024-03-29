import time
import json
import paho.mqtt.client as mqtt
import requests
import csv
from datetime import datetime

# MQTT broker details
mqtt_broker = "mqtt.eclipse.org"
mqtt_port = 1883
mqtt_topic = "sensor_data"

# Replace these with your Netatmo API credentials
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
USERNAME = 'your_username'
PASSWORD = 'your_password'
DEVICE_ID = 'your_device_id'
access_token = ''

# Netatmo API URLs
AUTH_URL = 'https://api.netatmo.com/oauth2/token'
GET_DEVICES_URL = 'https://api.netatmo.com/api/getstationsdata'

# Authenticate and get an access token
def authenticate():
    auth_payload = {
        'grant_type': 'password',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'username': USERNAME,
        'password': PASSWORD,
        'scope': 'read_station'
    }

    response = requests.post(AUTH_URL, data=auth_payload)
    auth_data = response.json()

    if 'access_token' in auth_data:
        return auth_data['access_token']
    else:
        raise Exception("Authentication failed")

# Get sensor readings
def get_sensor_readings(access_token, device_id):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    params = {
        'device_id': device_id
    }

    response = requests.get(GET_DEVICES_URL, headers=headers, params=params)
    data = response.json()

    if 'body' in data and 'devices' in data['body']:
        return data['body']['devices']
    else:
        raise Exception("Failed to retrieve sensor readings")

# Function to publish sensor reading on MQTT
def publish_sensor_reading(client, topic, reading):
    payload = json.dumps({"sensor_reading": reading})
    client.publish(topic, payload, qos=2)
    print(f"Published: {payload}")

# Function to save sensor readings to CSV file
def save_to_csv(data):
    CSV_FILE = 'sensor_readings.csv'
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for module in data:
            module_name = module['module_name']
            dashboard_data = module['dashboard_data']

            temperature = dashboard_data.get('Temperature', 'N/A')
            humidity = dashboard_data.get('Humidity', 'N/A')

            # Save to CSV
            writer.writerow([timestamp, module_name, temperature, humidity])

# Callback when connection is established
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(mqtt_topic)

# Main script
if __name__ == "__main__":
    # Create MQTT client instance
    client = mqtt.Client()

    # Set the callback functions
    client.on_connect = on_connect

    # Connect to MQTT broker
    client.connect(mqtt_broker, mqtt_port, 60)

    # Loop to maintain the connection
    client.loop_start()

    try:
        while True:
            # Get sensor reading
            sensor_reading = get_sensor_readings(access_token, DEVICE_ID)

            # Save sensor readings to CSV file
            save_to_csv(sensor_reading)

            # Publish sensor reading on MQTT
            publish_sensor_reading(client, mqtt_topic, sensor_reading)

            # Wait for some time before the next reading
            time.sleep(30*60)

    except KeyboardInterrupt:
        print("Script terminated by user.")
        client.disconnect()
        client.loop_stop()
    except Exception as e:
        print(f"Error: {e}")
