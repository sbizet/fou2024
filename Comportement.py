import numpy as np
from Utils import *

from Comportements.Carre import Carre
from Comportements.Cercle import Cercle
from Comportements.VagabondDroit import VagabondDroit
from Comportements.InitPos import InitPos

class Comportement():
    def __init__(self):
        self.id = 0  # doit être choisi par l'utilisateur
        self.newId = True
        self.vX = 0
        self.vY = 0
        self.heightFou = 0
        self.widthFou = 0
        self.xPos = 0
        self.yPos = 0
        self.resolution = 10
        self.indexPause = 0
        self.enPause = False
        self.dureePause = 0
        self.vMinArduino = 25 # en dessous de 25 pas/s on considère une vitesse nulle
        self.vMaxArduino = 2000

        self.carre = None
        self.cercle = None
        self.vagabondDroit = None
        self.initPos = None

        self.fc = ""

    def maj(self):
        if(self.enPause):
            self.compteurPause(self.dureePause)
        else :
            if(self.id==0): # ARRET
                if(self.newId) :
                    self.vX = 0
                    self.vY = 0
            if(self.id == 1): # Initialisation de la position
                if(self.newId):
                    self.initPos = InitPos(self.resolution)
                self.initPos.fc = self.fc
                self.vX,self.vY,fin = self.initPos.maj(self.vX,self.vY,self.xPos,self.yPos)

                if (fin) :
                    self.newId = True
                    self.id = 0 # à changer ...

            if(self.id==2): # Carré
                if(self.newId) :
                    self.carre = Carre(self.resolution) # première occurence, on créé l'instance carré
                    self.carre.setParam(800,500,1000) # accel,vitesse,taille
                self.vX,self.vY,self.dureePause = self.carre.maj(self.vX,self.vY,self.xPos,self.yPos) # maj du comportement carré, avec renseignement sur la vitesse et la position en cours

            if(self.id == 3): # Cercle
                if(self.newId) :
                    self.cercle = Cercle(self.resolution) # première occurence, on créé l'instance
                    self.cercle.setParam(400,1000,0) # vitesse,taille,angle origine
                self.vX,self.vY,self.dureePause = self.cercle.maj() # maj du comportement cercle

            if(self.id == 4): # vagabond droit
                if(self.newId) :
                    self.vagabondDroit = VagabondDroit(self.resolution) # première occurence, on créé l'instance
                    self.vagabondDroit.setParam(0,0,0)
                self.vX,self.vY,self.dureePause = self.vagabondDroit.maj(self.vX,self.vY,self.xPos,self.yPos) # maj du comportement

            if(self.fc != "") : # sécurité sur les fins de course, il n'y a plus de comportement
                if(self.fc == "G1") : self.vX = 100
                if(self.fc == "G0") : self.vX = 0
                if(self.fc == "D1") : self.vX = -100
                if(self.fc == "D0") : self.vX = 0
                if(self.fc == "H1") : self.vY = 100
                if(self.fc == "H0") : self.vY = 0
                if(self.fc == "B1") : self.vY = -100
                if(self.fc == "B0") : self.vY = 0
            self.fc = "" # fin de course pris en compte, on réinitialise.

            self.vX,self.vY = self.miseEnForme(self.vX,self.vY)

            if (self.dureePause>0) :
                self.enPause = True

            self.newId = False

    def setId(self,_id):
        if(self.id != id) :
            self.newId = True
        else :
            self.newId = False
        self.id = _id

    def miseEnForme(self,vX,vY):
        if(abs(vX)<self.vMinArduino) :
            vX = 0
        if(abs(vX)>self.vMaxArduino) :
            vX = self.vMaxArduino

        if(abs(vY)<self.vMinArduino) :
            vY = 0
        if(abs(vY)>self.vMaxArduino) :
            vY = self.vMaxArduino
        return vX,vY

    def miseEnPause(self,dureePause):
        self.vX = 0
        self.vY = 0
        self.enPause = True
        self.dureePause = dureePause

    def compteurPause(self,dureePause):
        if (self.indexPause == dureePause) :
            self.indexPause = 0
            self.enPause = False
        else :
            self.indexPause += 1


if __name__ == '__main__':
    import time
    import csv
    comportement = Comportement()
    comportement.setId(3)
    tempStr = "t;xPos;yPos;vX;vY\n"
    t = 0

    while(1):
        comportement.maj()
        vX = comportement.vX
        vY = comportement.vY
        dx = calcNPas(vX)*10
        dy = calcNPas(vY)*10
        comportement.xPos += dx
        comportement.yPos += dy
        # le calcul des temps est fait ici par python et est approximatif.
        # en réalité c'est Arduino qui donnera le tempo et ces temps dt
        if(vX == 0 and vY == 0): dt = 0
        elif (vX == 0) : dt = dy/vY
        elif (vY == 0) : dt = dx/vX
        else : dt = dx/vX
        t+=dt
        print(t,comportement.xPos,comportement.yPos,vX,vY)
        tempStr += (str(t) + ";"
                + str(comportement.xPos) + ";"
                + str(comportement.yPos) + ";"
                + str(vX) + ";"
                + str(vY) + "\n")
        time.sleep(dt)

        if msvcrt.kbhit():
            with open('data.csv', 'w') as output:
                 output.write(tempStr)
            break
