/*
 * Termometro digitale
*/

// Includi le librerie per lo schermo LCD
#include <LiquidCrystal.h>

// Includi le librerie per il sensore di temperatura
#include <OneWire.h> 
#include <DallasTemperature.h>
#define ONE_WIRE_BUS 8
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// Definisci i parametri dello schermo LCD
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// Definisci il pin per il buzzer
const int BUZZER = 9;

// Definisci i valori di temperatura
float prev_temp=85.0;
float last_prev_temp=85.0;
float temp;

void setup() {
  // Imposta colonne e righe dello schermo LCD
  lcd.begin(16, 2);
  lcd.noBlink();

  // Inizializza il sensore per la temperatua
  sensors.begin();

  // Imposta il pin per il buzzer
  pinMode(BUZZER, OUTPUT);

  // Stampa messaggio di benvenuto (in realtà fornisce il tempo per inizializzare il sensore)
  lcd.print("READY");
  delay(1000);
  lcd.clear();
}


long int i = 0;
void loop() {
  // Leggi la temperatura
  sensors.requestTemperatures();
  temp = sensors.getTempCByIndex(0);

  // Visualizza la temperatura e aspetta 4 secondi 
  lcd.print(temp);
  delay(4000);
  lcd.clear();

  // Controlla se siamo a regime
  if(abs(temp-prev_temp)<0.1 &&
     abs(temp-last_prev_temp)<0.1) {

      // Fai suonare il buzzer e visualizza la temperatura
      tone(BUZZER, 1000);
      lcd.print(temp);
      delay(2000);

      // Spegni il buzzer (sono passati 2 secondi) ma continua a visualizzare il valore per altri 8 secondi
      noTone(BUZZER);
      delay(8000);

      // Pulisci lo schermo e setta la temperatura a 85.0
      lcd.clear();
      temp=85.0;
  }

  // Salva le temperature per controllare se arriviamo a regime
  if(i==0) {
    prev_temp=temp;
  }
  else if (i>0) {
    last_prev_temp = prev_temp;
    prev_temp = temp;
  }
  i++;
}
