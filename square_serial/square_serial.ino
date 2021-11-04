void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);  
}

void loop() {
  // put your main code here, to run repeatedly:

  for(int i=0;i<10;i++){
    Serial.print("0\n");
    delay(100);
  }

  for(int i=0;i<10;i++){
    Serial.print("255\n");
    delay(100);
  }
  
}
