import paho.mqtt.client as mqtt
import json
import csv
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to the topic where the ThingML model will publish plant state
    client.subscribe("thingml/plant_state")

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    plant_state = payload.get("plant_state", None)
    print(f"Received Plant State: {plant_state}")

def send_pixel_counts(client, light_green_pixel_count, green_pixel_count, dark_green_pixel_count):
    message = {
        "light_green_pixel_count": light_green_pixel_count,
        "green_pixel_count": green_pixel_count,
        "dark_green_pixel_count": dark_green_pixel_count
    }
    # Publish the pixel counts to the topic where the ThingML model is subscribed
    client.publish("thingml/pixel_counts", json.dumps(message))

def read_pixel_counts_from_csv(file_path):
    pixel_counts_list = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            light_green_pixel_count = int(row.get("light_green_pixel_count", 0))
            green_pixel_count = int(row.get("green_pixel_count", 0))
            dark_green_pixel_count = int(row.get("dark_green_pixel_count", 0))
            pixel_counts_list.append({
                "light_green_pixel_count": light_green_pixel_count,
                "green_pixel_count": green_pixel_count,
                "dark_green_pixel_count": dark_green_pixel_count
            })
    return pixel_counts_list

def main():
    # Configure MQTT broker information
    broker_address = "your_mqtt_broker_address"
    client = mqtt.Client()

    # Set up callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT broker
    client.connect(broker_address, 1883, 60)

    try:
        # Example CSV file path
        csv_file_path = "path/to/your/pixel_counts.csv"

        # Read pixel counts from CSV file
        pixel_counts_list = read_pixel_counts_from_csv(csv_file_path)

        # Iterate through the list and send pixel counts to ThingML model via MQTT
        for counts in pixel_counts_list:
            send_pixel_counts(client, counts["light_green_pixel_count"], counts["green_pixel_count"], counts["dark_green_pixel_count"])
            time.sleep(1)  # Add a delay if needed

        # Wait for incoming messages (plant state) - the on_message callback will be invoked
        client.loop_forever()

    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
