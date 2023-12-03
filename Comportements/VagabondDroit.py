import sys
sys.path.append('..')
from Utils import *
from random import randint

class VagabondDroit():
    def __init__(self,res):
        self.phase = -1
        self.goto = Goto(res)
    def setParam(self,p0,p1,p2):
        None
    def maj(self,vX_old,vY_old,xPos,yPos):
        dureePause = 0
        if(self.phase == -1) :
            self.vMax = randint(200, 1800)
            self.xCible = randint(30,10000)
            self.yCible = randint(30,5000)
            self.goto.setParam(1000,self.vMax,self.xCible,self.yCible)
            self.phase = 0
            print("Vagabond cible x = " + str(self.xCible),
                "y = " + str(self.yCible),
                "vMax = " + str(self.vMax))
        if(self.phase == 0):
            vX,vY = self.goto.maj(vX_old,vY_old,xPos,yPos)
            if(vX == 0 and vY == 0): # fin de la phase quand les vitesses sont redevenues nulles
                self.goto.init()
                self.phase = 1
        if (self.phase == 1) :
            dureePause = 30
            self.phase = -1
        return vX,vY,dureePause
