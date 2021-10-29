// Variable resistance stretch cord testing code! Made Jan 29 by Erin Gee for Instructables

int sensorPin = A0;    // select the input pin for the potentiometer
float sensorValue;

float lettura1=0;
float lettura2=0;
float lettura3=0;
float lettura4=0;
float lettura5=0;
int i=0;

const int buzzer = 10;

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  pinMode(buzzer, OUTPUT); 
}

void loop() {
  
  // read the value from the sensor:
  sensorValue = analogRead(sensorPin);
  if (i==0){
    lettura1=sensorValue;
    i++;
  }
  else if (i==1) {
    lettura2=sensorValue;
    i++;
  }
  else if (i==2) {
    lettura3=sensorValue;
    i++;
  }
  else if (i==3) {
    lettura4=sensorValue;
    i++;
  }
  else if (i==4) {
    lettura5=sensorValue;
    i=0;
  
    //write these values to Serial Window
    Serial.println((lettura1+lettura2+lettura3+lettura4+lettura5)/5.0);
  }
  
  /* 
  if (sensorValue>700){
    tone(buzzer, 1000);
    delay(10);
    noTone(buzzer);
  }
  */
  
  delay(5);                
}
