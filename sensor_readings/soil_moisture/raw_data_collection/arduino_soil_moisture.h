#include <SPI.h>
#include <SD.h>
#include <PubSubClient.h>
#include <Ethernet.h>

// Ethernet shield settings
byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
IPAddress broker(192, 168, 1, 100); // Replace with your MQTT broker's IP address

const int chipSelect = 4;
int sensorPins[] = {A0, A1};
unsigned long startTime;
unsigned long lastReadingTime = 0;

EthernetClient ethClient;
PubSubClient client(ethClient);

void setup() {
  Serial.begin(9600);

  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    while (1);
  }
  
  // Initialize Ethernet and MQTT client
  Ethernet.begin(mac);
  client.setServer(broker, 1883);

  startTime = millis();  // Record the start time of the experiment
  Serial.println("Card initialized.");
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }

  client.loop();

  if (millis() - lastReadingTime >= 24 * 60 * 60 * 1000) { // Check if 24 hours have passed
    File dataFile = SD.open("datalog.csv", FILE_WRITE);
    
    unsigned long timePassed = millis() - startTime;
    int weeksPassed = timePassed / (7 * 24 * 60 * 60 * 1000); // Calculate number of weeks passed
    
    int numSensors = 2 + (2 * weeksPassed); // 2 sensors in the first week, and 2 more every week
    if (numSensors > 10) numSensors = 10;  // Cap at 10 sensors

    if (dataFile) {
      for (int i = 0; i < numSensors; i++) {
        
        // Do 3 readings
        for (int j = 0; j < 3; j++) {
          int sensorValue = analogRead(sensorPins[i]);
          float calculatedHumidity = map(sensorValue, 0, 1023, 0, 100); 
          
          dataFile.print(millis());
          dataFile.print(",");
          dataFile.print("A");
          dataFile.print(i);
          dataFile.print(",");
          dataFile.print(sensorValue);
          dataFile.print(",");
          dataFile.println(calculatedHumidity);

          publishToMQTT(i, sensorValue, calculatedHumidity);
          
          delay(150);  // Delay between each reading
        }

        // Do 10 readings
        for (int j = 0; j < 10; j++) {
          int sensorValue = analogRead(sensorPins[i]);
          float calculatedHumidity = map(sensorValue, 0, 1023, 0, 100); 
          
          dataFile.print(millis());
          dataFile.print(",");
          dataFile.print("A");
          dataFile.print(i);
          dataFile.print(",");
          dataFile.print(sensorValue);
          dataFile.print(",");
          dataFile.println(calculatedHumidity);

          publishToMQTT(i, sensorValue, calculatedHumidity);
          
          delay(150);  // Delay between each reading
        }

        delay(1000);  // Delay before reading from the next sensor
      }

      dataFile.close();
      Serial.println("Data saved");
    } else {
      Serial.println("Error writing to datalog.csv");
    }

    lastReadingTime = millis(); // Update the last reading time
  }

  delay(24*60*60*1000);  
}

void publishToMQTT(int sensorIndex, int sensorValue, float calculatedHumidity) {
  String topic = "sensor_data/A" + String(sensorIndex);
  String payload = "{\"Timestamp\": " + String(millis()) + ", \"SensorValue\": " + String(sensorValue) + ", \"Humidity\": " + String(calculatedHumidity) + "}";
  
  client.publish(topic.c_str(), payload.c_str());
  Serial.println("Published to MQTT: " + topic + " - " + payload);
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("arduino-client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}
