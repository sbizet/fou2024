import sys
sys.path.append('..')
from Utils import *

class Carre():
    def __init__(self,res):
        self.phase = -1
        self.taille = 1000
        self.aMax = 1000
        self.vMax = 500
        self.goto = Goto(res)

    def setParam(self,aMax,vMax,taille):
        self.taille = taille
        self.aMax = aMax
        self.vMax = vMax

    def maj(self,vX_old,vY_old,xPos,yPos):
        dureePause = 0
        if(self.phase == -1):
            self.goto.setParam(self.aMax,self.vMax,self.taille+xPos,yPos)
            self.phase = 0
            print("Carré Phase = " + str(self.phase))
        if(self.phase == 0):
            vX,vY = self.goto.maj(vX_old,vY_old,xPos,yPos)
            if(vX == 0 and vY == 0): # fin de la phase quand les vitesses sont redevenues nulles
                self.goto.init()
                self.goto.setParam(self.aMax,self.vMax,xPos,self.taille+yPos)
                self.phase = 1
                print("Carré Phase = " + str(self.phase))
        if(self.phase == 1):
            vX,vY = self.goto.maj(vX_old,vY_old,xPos,yPos)
            if(vX == 0 and vY == 0):
                self.goto.init()
                self.goto.setParam(self.aMax,self.vMax,xPos-self.taille,yPos)
                self.phase = 2
                print("Carré Phase = " + str(self.phase))
        if(self.phase == 2):
            vX,vY = self.goto.maj(vX_old,vY_old,xPos,yPos)
            if(vX == 0 and vY == 0):
                self.goto.init()
                self.goto.setParam(self.aMax,self.vMax,xPos,yPos-self.taille)
                self.phase = 3
                print("Carré Phase = " + str(self.phase))
        if(self.phase == 3):
            vX,vY = self.goto.maj(vX_old,vY_old,xPos,yPos)
            if(vX == 0 and vY == 0):
                self.phase = 4
                print("Carré Phase = " + str(self.phase))
        if(self.phase == 4):
            self.goto.init()
            vX = 0
            vY = 0
            dureePause = 30
            self.phase = -1
        return vX,vY,dureePause
