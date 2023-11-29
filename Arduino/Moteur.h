#include "Arduino.h"
#include <DIO2.h>

class Moteur
{
  private :
    GPIO_pin_t pinStep = DP2;
    GPIO_pin_t pinDir = DP3;
    GPIO_pin_t MS1 = DP4;
    GPIO_pin_t MS2 = DP5;
    GPIO_pin_t MS3 = DP6;
    boolean invert = false;
    int nTop = 0;
    int nTopTemp = 0;
    int iTop = 0;
    byte param = 0;
    boolean nTopValid = false;
    int resolution = 10;
    int iPas = 0;


  public :
    Moteur();
    void setPin(GPIO_pin_t _pinStep, GPIO_pin_t _pinDir,GPIO_pin_t,GPIO_pin_t,GPIO_pin_t,boolean);
    boolean maj();
    void setParam(byte _octet0);
    void setNTopHigh(byte _octet0);
    void setNTopLow(byte _octet1);
};
