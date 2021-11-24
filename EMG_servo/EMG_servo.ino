// Importa la libreria per il servomotore
#include <Servo.h>

// Definisci threshold (varia da persona a persona)
#define THRESHOLD 80

// Definisci pin su cui collegare il modulo EMG (Analog 0)
#define EMG_PIN 0

// Definisci il pin su cui collegare il servomotore (Digital 3)
#define SERVO_PIN 3

// Definisci il servomotore
Servo SERVO_1;

// Definisci variabile booleana per controllare il servomotore
bool opened = true;

// Definisci variabile per lettura segnale EMG
int value;

/*-------------------------------- void setup ------------------------------------------------*/

void setup(){
  
  // Inizializza la connessione seriale a 9600 BAUD 
  Serial.begin(9600);
  
  // Associa il servomotore al pin definito sopra
  SERVO_1.attach(SERVO_PIN);
}

/*--------------------------------  void loop  ------------------------------------------------*/

void loop(){

  // Leggi il valore dal sensore EMG
  value = analogRead(EMG_PIN);

  // Se il valore letto e' minore della soglia e la mano e' chiusa, setta il motore a 180 gradi
  if(value < THRESHOLD && opened == false){
    SERVO_1.write(179);
    opened = true;
  }

  // Se il valore letto e' maggiore della soglia e la mano e' aperta, setta il motore a 0 gradi
  else if (value >= THRESHOLD && opened == true) {
    SERVO_1.write(0);
    opened = false;
  }

  // Manda il valore letto sulla seriale (utile per scegliere la soglia giusta per ciascun soggetto e/o configurazione)
  Serial.println(value);
  delay(100);
}
