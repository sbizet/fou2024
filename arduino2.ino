#include <DIO2.h>
#include "Moteur.h"

GPIO_pin_t MS1X = DP12;
GPIO_pin_t MS2X = DP13;
GPIO_pin_t MS3X = DP2;

GPIO_pin_t MS1Y = DP5;
GPIO_pin_t MS2Y = DP10;
GPIO_pin_t MS3Y = DP11;

GPIO_pin_t pinStepX = DP4;
GPIO_pin_t pinDirX = DP7;
GPIO_pin_t pinStepY = DP3;
GPIO_pin_t pinDirY = DP6;

GPIO_pin_t pinEnable = DP8;

Moteur moteurX;
Moteur moteurY;

void setup() {
  Serial.begin(115200);
  initMoteur();
  initTimer();
}

void loop() {
  if (Serial.available() > 0) {
    byte lu = Serial.read();
    if (bitRead(lu, 7) == 0) {
      if (bitRead(lu, 6) == 0) {
        moteurX.setParam(lu);
        moteurX.setNTopHigh(lu);
      }
      else{
        moteurX.setNTopLow(lu);
      }
    }
    else {
      if (bitRead(lu, 6) == 0) {
        moteurY.setParam(lu);
        moteurY.setNTopHigh(lu);
      }
      else{
        moteurY.setNTopLow(lu);
      }
    }
  }
}

void initTimer() {
  TCCR2A = 0;// set entire TCCR2A register to 0
  TCCR2B = 0;// same for TCCR2B
  TCNT2  = 0;//initialize counter value to 0
  
  OCR2A = 24;// = (16*10^6) / (80000*8) - 1 
  TCCR2A |= (1 << WGM21); // turn on CTC mode
  TCCR2B |= (1 << CS21);   // Set CS21 bit for 8 prescaler
  TIMSK2 |= (1 << OCIE2A); // enable timer compare interrupt
}

ISR(TIMER2_COMPA_vect) { // s’exécute 80000 fois par secondes
  if(moteurX.maj()) Serial.write(0);
  if(moteurY.maj()) Serial.write(128);
}

void initMoteur() {
  moteurX.setPin(pinStepX, pinDirX, MS1X, MS2X, MS3X, false); // = Z sur le shield
  moteurY.setPin(pinStepY, pinDirY, MS1Y, MS2Y, MS3Y, true);
  pinMode2f( pinEnable, OUTPUT );
  digitalWrite2f( pinEnable, LOW ); // logique inversée
}
