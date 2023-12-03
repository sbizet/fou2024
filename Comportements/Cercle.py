import sys
sys.path.append('..')
from Utils import *

class Cercle():
    def __init__(self,res):
        self.taille = 1000
        self.vMax = 500
        self.angle = 0

    def setParam(self,vMax,taille,angleOrigine):
        self.dAngle = 0.0228*vMax/taille # très approximatif ...
        self.vMax = vMax
        self.angle = angleOrigine

    def maj(self):
        self.angle += self.dAngle
        vX = self.vMax * np.cos(self.angle)
        vY = self.vMax * np.sin(self.angle)
        return vX,vY,0
