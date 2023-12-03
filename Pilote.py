from Comportement import Comportement
from threading import Thread
from InterfaceSerie import InterfaceSerie
import time
from Utils import *

class Pilote :
    def __init__(self):
        self.ser = InterfaceSerie(115200)
        self.ser.readSerialStart()

        self.widthFou = 10000 # nombre de pas total à l'horizontale ... à déterminer
        self.heightFou = 5000 # nombre de pas total à la verticale ... à déterminer
        self.xPos = self.widthFou/2 # position initiale prise au milieu avant détection des fins de course
        self.yPos = self.heightFou/2
        self.vMin = 25 # en dessous de 25 pas/s on considère une vitesse nulle
        self.vMax = 2000 # vitesse maximale au delà de laquelle des pertes de pas sont possibles
        self.resolution = 10 # nombre de cycles effectués par Arduino entre 2 top série. Cette résolution doit être la même que celle réglée dans Arduino
        self.fTimer = 80000 # fréquence du timer Arduino. Cette valeur est déterminée dans le code Arduino

        self.comportement = Comportement()
        self.comportement.vMin = self.vMin
        self.comportement.vMax = self.vMax
        self.comportement.resolution = self.resolution
        self.comportement.widthFou = self.widthFou
        self.comportement.heightFou = self.heightFou
        self.comportement.xPos = self.xPos
        self.comportement.yPos = self.yPos
        self.threadComportement = None
        self.xValid = False
        self.yValid = False
        self.axesXetY = False
        self.octetFc = 0
        self.demarrage()

    def gestionFc(self,oldOctetFc,octetFc):
        # recalage des positions en fin de fin de course

        if((octetFc >> 0) & 1) : # à gauche
            self.comportement.fc = "G1"
        elif ((oldOctetFc >> 0) & 1) :
            self.comportement.fc = "G0"
            self.xPos = 0
            self.comportement.xPos = self.xPos

        if((octetFc >> 1) & 1) : # à droite
            self.comportement.fc = "D1"
        elif ((oldOctetFc >> 1) & 1) :
            self.comportement.fc = "D0"
            self.xPos = self.widthFou
            self.comportement.xPos = self.xPos

        if((octetFc >> 2) & 1) : # en haut
            self.comportement.fc = "H1"
        elif ((oldOctetFc >> 2) & 1) :
            self.comportement.fc = "H0"
            self.yPos = 0
            self.comportement.yPos = self.yPos

        if((octetFc >> 3) & 1) : # en bas
            self.comportement.fc = "B1"
        elif ((oldOctetFc >> 3) & 1) :
            self.comportement.fc = "B0"
            self.yPos = self.heightFou
            self.comportement.yPos = self.yPos

    def topInSerie(self,octet) :
        oldVX,oldVY = self.comportement.vX,self.comportement.vY
        if(((octet[0] >> 7) & 1)) : axe = "Y"
        else : axe = "X"
        if (oldVX != 0  and oldVY !=0) : # les vitesses des deux axes sont à prendre en compte
            self.axesXetY = True
            if(axe == "X") : self.xValid = True
            if(axe == "Y") : self.yValid = True
            if(self.xValid == False or self.yValid == False):
                self.comportement.maj() # maj une fois sur deux quand l'un des axe n'a pas encore été validé
            if(self.xValid == True and self.yValid == True): # réinitialisation des validations
                self.xValid = False
                self.yValid = False
        else :
            if(not self.axesXetY) : # pas de maj si on était juste avant sur 2 vitesses X et Y à prendre en compte: on prend en compte les 2 axes une dernière fois
                self.comportement.maj() # l'une des vitesse est à 0 la mise à jour a lieu systématiquement
            self.axesXetY = False
            self.xValid = False
            self.yValid = False

        forceX,forceY = False,False

        # Prise en compte des fins de course
        oldOctetFc = self.octetFc
        self.octetFc = octet[0]&0b1111
        self.gestionFc(oldOctetFc,self.octetFc)

        vX,vY = self.comportement.vX,self.comportement.vY
        if(oldVX != 0 and  vX== 0 and oldVY == 0 and vY!=0): # pour éviter un arrêt intempestif
            forceY = True
            self.xValid = True
            self.yValid = True
        if(oldVY != 0 and vY == 0 and oldVX == 0 and vX!=0): # pour éviter un arrêt intempestif
            forceX = True
            self.xValid = True
            self.yValid = True
        if(oldVX == 0 and vX != 0): # pour relancer l'axe X
            forceX = True
        if(oldVY == 0 and vY != 0): # pour relancer l'axe X
            forceY = True

        if(axe == "X" or forceX):
            self.envoyer('X')
        if(axe == "Y" or forceY):
            self.envoyer('Y')

        if(self.comportement.enPause) :
            if self.threadComportement == None:
                self.threadComportement = Thread(target=self.threadPause)
                self.threadComportement.start()

    def threadPause(self):
        self.arret()
        print("Thread Pause démarré ...\n")
        while (self.comportement.enPause):
            self.comportement.maj()
            time.sleep(0.1)
        self.threadComportement=None
        self.demarrage()

    def arret(self):
        envoi = self.calcEnvoi(0,0)
        self.ser.envoi(envoi)
        envoi = self.calcEnvoi(1,0)
        self.ser.envoi(envoi)
        print("ARRET")

    def demarrage(self):
        print("START")
        self.comportement.maj()
        if(self.comportement.vX != 0)  :
            self.envoyer('X')
        if(self.comportement.vY != 0)  :
            self.envoyer('Y')

    def envoyer(self,axe):
        if (axe == 'X'):
            envoi = self.calcEnvoi(0,self.comportement.vX)
            self.ser.envoi(envoi)
            self.xPos += calcNPas(self.comportement.vX)*self.resolution
            self.comportement.xPos = self.xPos
            #print('vX : ' +str(int(self.comportement.vX)) + '\tenvoi X = '+ bin(envoi[0]) + " " + bin(envoi[1]) + "\txPos = " + str(self.xPos))
        if (axe == 'Y'):
            envoi = self.calcEnvoi(1,self.comportement.vY)
            self.ser.envoi(envoi)
            self.yPos += calcNPas(self.comportement.vY)*self.resolution
            self.comportement.yPos = self.yPos
            #print('vY : ' +str(int(self.comportement.vY)) + '\tenvoi Y = '+ bin(envoi[0]) + " " + bin(envoi[1]) + "\tyPos = " + str(self.yPos))

    def setVitesse(self,vX,vY):
        oldVX,oldVY = self.comportement.vX,self.comportement.vY
        self.comportement.vX,self.comportement.vY = self.comportement.miseEnForme(vX,vY)
        if(oldVX == 0 and self.comportement.vX != 0):
            self.topInSerie(b'\x00')
        if(oldVY == 0 and self.comportement.vY != 0):
            self.topInSerie(b'\x80')

    def setVitesseX(self,v):
        self.setVitesse(v,self.comportement.vY)

    def setVitesseY(self,v):
        self.setVitesse(self.comportement.vX,v)

    def calcEnvoi(self,x_ou_y,v) :
        if (v<0) : dir = 0
        else : dir = 1
        v = int(abs(v))
        octet0=0
        octet0 |= (x_ou_y<<7)
        octet0 |= (dir<<5)

        redPas = calcRedPas(v)
        if (redPas == 1/2) : #HALF STEP
            octet0 |= (1<<4)
        elif (redPas == 1/4): #QUARTER STEP
            octet0 |= (1<<3)
        elif (redPas == 1/8) : #EIGHTH STEP
            octet0 |= (1<<4)
            octet0 |= (1<<3)
        elif (redPas == 1/16) : #1/16 de pas
            octet0 |= (1<<4)
            octet0 |= (1<<3)
            octet0 |= (1<<2)

        if(v<self.vMin) :
            nTop = 0
        else :
            nTop = int(redPas * self.fTimer / v);
        if(nTop & 1 << 7 != 0) : octet0 |= (1<<1)
        if(nTop & 1 << 6 != 0) : octet0 |= (1<<0)

        octet1=0
        octet1 |= (x_ou_y<<7)
        octet1 |= (1<<6)
        for i in range(6):
            if(nTop & 1 << i != 0) : octet1 |= (1<<i)
        b = bytearray([octet0,octet1])
        return b

    def majSerie(self):
        octet = self.ser.majSerie()
        if (not octet == None):
            self.topInSerie(octet)

if __name__ == '__main__':
    pilote = Pilote()
    # test calcEnvoi
    print("Test CalcEnvoi :")
    print(pilote.calcEnvoi(0,100)[0],pilote.calcEnvoi(0,100)[1])
    print(" _________________________ ")
    # test topInSerie
    pilote.comportement.vX = 100
    pilote.comportement.vY = 0
    oldXPos = pilote.xPos
    pilote.topInSerie(b'\x00')
    print("Test TopSerie :")
    print(oldXPos,pilote.xPos)
