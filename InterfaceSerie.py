import serial
import serial.tools.list_ports

import time
from SimulArduino import SimulArduino

class InterfaceSerie:
    def __init__(self, baud = 115200):
        self.simulArduino = None
        self.start = False
        self.simul = False
        comlist = serial.tools.list_ports.comports()
        connected = []
        for element in comlist:
            connected.append(element.device)
        if(len(connected) == 0) :
            self.simul = True
        if (not self.simul):
            print("Ports COM connectés : " + str(connected))
            port = connected[-1]
            print('Connection en cours sur le Port: ' + str(port) + ' à ' + str(baud) + ' Baud.')
            try:
                self.ser = serial.Serial(port, baud, timeout=4)
                print('Connecté sur le Port ' + str(port) + ' à ' + str(baud) + ' Baud.')
            except:
                print("Echec de la connexion sur le Port " + str(port) + ' à ' + str(baud) + ' Baud.')
                self.simul = True

        if(self.simul) :
            print("Pas d'Arduino ou liaison série défectueuse, nous allons la simuler")
            self.simulArduino = SimulArduino()


    def readSerialStart(self):
        if(not self.simul):
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            print("Liaison série démarrée ...")

        self.start = True

    def majSerie(self):
        retour = None
        if (self.start) :
            if(self.simul):
                self.simulArduino.timer()
                octetRecu = self.simulArduino.read()
                if(octetRecu>=0):
                    retour = octetRecu.to_bytes(1, 'big')
            else:
                if (self.ser.in_waiting) :
                    octetRecu = self.ser.read()
                    retour = octetRecu
        return retour

    def envoi(self,b):
        if(self.simul):
            self.simulArduino.write(b)
        else:
            self.ser.write(b)

# testUnitaire
if __name__ == '__main__':
    ser = InterfaceSerie(115200)
    ser.readSerialStart()
    b = bytearray([25,100])
    time.sleep(3) # il faut attendre 3 secondes que la liaison série soit prête ... à améliorer.
    ser.envoi(b)

    index=0
    while (1) :
        octet = ser.majSerie()
        if (not octet == None):
            print(index,octet)
            ser.envoi(b)
            index+=1
            if(index==1000) : break
