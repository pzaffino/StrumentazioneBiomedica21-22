#include <Wire.h>
#include "MAX30100_PulseOximeter.h"
#include <OneWire.h>
#include <DallasTemperature.h>

#define REPORTING_PERIOD_MS     1000

// DEFINIZIONE PIN
#define BUZZER 3
#define ESTENSIMETRO A3
#define TEMPERATURA 5

// PULSOSSIMETRO
//PulseOximeter pox;
uint32_t tsLastReport = 0;

// TEMPERATURA
OneWire oneWire(TEMPERATURA);
DallasTemperature temperature_sensors(&oneWire);
float temperature;
float o2=0;
int hr=0; 
float ecg;

// Callback (registered below) fired when a pulse is detected
void onBeatDetected()
{
    tone(BUZZER, 1000);
    delay(200);
    noTone(BUZZER);
}

void setup()
{
    Serial.begin(9600);

    // PIN MODE
    pinMode(BUZZER, OUTPUT);

    // SENSORE TEMPERATURA
    temperature_sensors.begin();
    /*
    // Initialize the PulseOximeter instance
    Serial.print("Initializing pulse oximeter..");
    if (!pox.begin()) {
        //Serial.println("FAILED");
        for(;;);
    } else {
        //Serial.println("SUCCESS");
    }

    //pox.setOnBeatDetectedCallback(onBeatDetected);
    */
}

void loop()
{
    //pox.update();
    if (millis() - tsLastReport > REPORTING_PERIOD_MS) {

        // TEMPERATURA
        temperature_sensors.requestTemperatures(); // Command to get temperature readings
        temperature = temperature_sensors.getTempCByIndex(0);

        // PULSOSSIMETRO
        //hr = (int)pox.getHeartRate();
        //o2 = (float)pox.getSpO2();
        
        tsLastReport = millis();
    }

    // ESTENSIMETRO
    float estensimetro_value = analogRead(ESTENSIMETRO)/7.0;
    delay(10);

    if((digitalRead(10) == 1)||(digitalRead(11) == 1)){
      //Serial.println('!');
    }
    else{
    // send the value of analog input 0:
    ecg = analogRead(A0)/3.0;
    }
    delay(5);
    

    // HR,O2, estensimetro
    Serial.print(hr);
    Serial.print(",");
    Serial.print(o2);
    Serial.print(",");
    Serial.print(estensimetro_value);
    Serial.print(",");
    Serial.print(temperature);
    Serial.print(",");
    Serial.println(ecg);


}
