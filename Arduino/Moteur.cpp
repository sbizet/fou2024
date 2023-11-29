#include <DIO2.h>

#include "Arduino.h"
#include "Moteur.h"

Moteur::Moteur()
{}

void Moteur::setPin(GPIO_pin_t _pinStep, GPIO_pin_t _pinDir, GPIO_pin_t _MS1, GPIO_pin_t _MS2, GPIO_pin_t _MS3, boolean _invert) {
  pinStep = _pinStep;
  pinDir = _pinDir;
  pinMode2f(pinStep, OUTPUT);
  pinMode2f(pinDir, OUTPUT);
  digitalWrite2f(pinDir, HIGH);
  digitalWrite2f(pinStep, HIGH);
  MS1 = _MS1;
  MS2 = _MS2;
  MS3 = _MS3;
  pinMode2f (MS1, OUTPUT); pinMode2f (MS2, OUTPUT); pinMode2f (MS3, OUTPUT);
  digitalWrite2f(MS1, LOW);
  digitalWrite2f(MS2, LOW);
  digitalWrite2f(MS3, LOW);
  invert = _invert;

}

boolean Moteur::maj() {
  boolean retour =false;
  if (nTop > 0) {
    if (iTop == nTop >> 1) {
      digitalWrite2f(pinStep, LOW);
    }
    if (iTop == 0) {
      digitalWrite2f(pinStep, HIGH);
      iPas++;
      if(iPas == resolution) {
        retour = true;
        iPas = 0;
      }
      iTop = nTop;
    }
    iTop--;
  }
  else iTop = 0;
  return retour;
}

void Moteur::setParam(byte _octet0) {
  byte paramEnCours = _octet0&60;
  if(param != paramEnCours) {
    byte dir = bitRead(_octet0, 5);
    if (invert) digitalWrite2f(pinDir, !dir);
    else digitalWrite2f(pinDir, dir);
  
    byte _etatMS1 = bitRead(_octet0, 4);
    byte _etatMS2 = bitRead(_octet0, 3);
    byte _etatMS3 = bitRead(_octet0, 2);
  
    digitalWrite2f(MS1, _etatMS1);
    digitalWrite2f(MS2, _etatMS2);
    digitalWrite2f(MS3, _etatMS3);

    param = paramEnCours;
  }

}

void Moteur::setNTopHigh(byte _octet0) {
  nTopTemp = (_octet0 & 3) << 6;
}

void Moteur::setNTopLow(byte _octet1) {
  nTop = nTopTemp + (_octet1 & 63);
}
