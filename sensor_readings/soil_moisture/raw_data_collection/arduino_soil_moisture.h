#include <SPI.h>
#include <SD.h>

const int chipSelect = 4;
int sensorPins[] = {A0, A1, A2, A3, A4, A5, A6, A7, A8, A9};
unsigned long startTime;
unsigned long lastReadingTime = 0;

void setup() {
  Serial.begin(9600);

  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    while (1);
  }
  
  startTime = millis();  // Record the start time of the experiment
  Serial.println("Card initialized.");
}

void loop() {
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

  delay(1000);  // Sleep for a bit to avoid constantly checking the time
}
