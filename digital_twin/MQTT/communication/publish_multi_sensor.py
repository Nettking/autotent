import time
import json
import csv
from datetime import datetime
import paho.mqtt.client as mqtt

# MQTT broker details
mqtt_broker = "mqtt.eclipse.org"
mqtt_port = 1883
mqtt_topic = "sensor_data"

# Function to read sensor data from CSV file
def read_sensor_data(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            yield row

# Function to convert timestamp to Unix timestamp
def convert_to_unix_timestamp(timestamp_str, timezone):
    timestamp_format = "%Y/%m/%d %H:%M:%S"
    dt = datetime.strptime(timestamp_str, timestamp_format)
    dt = dt.replace(tzinfo=timezone)
    return int(dt.timestamp())

# Function to publish sensor reading on MQTT
def publish_sensor_reading(client, topic, reading):
    payload = json.dumps(reading)
    client.publish(topic, payload, qos=2)
    print(f"Published: {payload}")

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
        # Replace the file path with the actual path to your CSV file
        sensor_data_file = "path/to/your/sensor_data.csv"

        for sensor_reading in read_sensor_data(sensor_data_file):
            timestamp = convert_to_unix_timestamp(sensor_reading['Timestamp'], "Europe/Oslo")
            sensor_reading['Timestamp'] = timestamp

            # Publish sensor reading on MQTT
            publish_sensor_reading(client, mqtt_topic, sensor_reading)

            # Wait for some time before the next reading
            time.sleep(5)

    except KeyboardInterrupt:
        print("Script terminated by user.")
        client.disconnect()
        client.loop_stop()
