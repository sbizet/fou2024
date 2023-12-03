import sys
sys.path.append('..')
from Utils import *

class InitPos():
    def __init__(self,res):
        self.phase = 0
        self.goto = Goto(res)
        self.vX = -1000
        self.vY = -500
        self.fc = ""
        self.x0Atteint = False
        self.y0Atteint = False
        self.fin = False

    def maj(self,vX_old,vY_old,xPos,yPos):
        if(self.phase==0):
            if(self.fc == "G0"):
                self.x0Atteint = True
                self.vX = 0
                print("X0 atteint")
            if(self.fc == "H0"):
                self.y0Atteint = True
                self.vY = 0
                print("Y0 atteint")
            if(self.x0Atteint and self.y0Atteint) :
                print("La position est validée")
                self.phase = 1
                self.goto.setParam(1000,1000,2000,1000)
        if(self.phase == 1) :
            self.vX,self.vY = self.goto.maj(vX_old,vY_old,xPos,yPos)
            if(self.vX == 0 and self.vY == 0): # fin de la phase quand les vitesses sont redevenues nulles
                self.phase = 2
        if(self.phase==2):
            self.vX = 0
            self.vY = 0
            self.fin = True
        return self.vX,self.vY,self.fin
