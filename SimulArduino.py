import asyncio
import time

class SimulArduino :
    def __init__(self):
        self.resolution = 10
        self.arret = True
        self.nTopX = 0
        self.nTopY = 0
        self.dtX = 0
        self.dtY = 0
        self.toX = time.time()
        self.toY = time.time()
        self.toTimer = time.time()
        self.octetEnvoi = 0

    def write(self,b):
        x_ou_y = (b[0] >> 7) & 1
        nTop = 0
        nTop |= ((b[0] >> 1) & 1)<<7
        nTop |= ((b[0] >> 0) & 1)<<6
        for i in range(6):
            nTop |= ((b[1] >> i) & 1)<<i
        if(x_ou_y == 0) :
            self.nTopX = nTop
        else :
            self.nTopY = nTop

        if(self.nTopX == 0 and self.nTopY == 0): self.arret = True
        else : self.arret = False

        if(self.nTopX>0):
            self.dtX = self.resolution*self.nTopX/80000
        else :
            self.dtX = 0
            self.toX = time.time()

        if(self.nTopY>0):
            self.dtY = self.resolution*self.nTopY/80000
        else :
            self.dtY = 0
            self.toY = time.time()

    def read(self):
        retour = self.octetEnvoi
        self.octetEnvoi = -1
        return retour

    def timer(self):
        maintenant = time.time()
        if(self.dtX>0):
            if(maintenant-self.toX>2*self.dtX):
                self.toX = maintenant
                self.octetEnvoi = 0
            elif(maintenant-self.toX>self.dtX):
                self.toX = self.toX+self.dtX
                self.octetEnvoi = 0

        if(self.dtY>0):
            if(maintenant-self.toY>2*self.dtY):
                self.toY = maintenant
                self.octetEnvoi = 0
            elif(maintenant-self.toY>self.dtY and self.octetEnvoi == -1):
                self.toY = self.toY+self.dtY
                self.octetEnvoi = 128


# testUnitaire
if __name__ == '__main__':
    simulArduino = SimulArduino()
    b1 = bytearray([25,100]) # sur X : 25 = 0001 1001 et 100 = 0110 0100 -> nTop = 100
    b2 = bytearray([153,203]) # sur Y : 153 = 1001 1001 et 203 = 1100 1011 -> nTop = 75
    simulArduino.write(b1) # envoyé à l'Arduino simulée par le programme
    index = 0

    while (1) :
        simulArduino.timer()
        octetRecu = simulArduino.read() # envoyé par Arduino simulée, lu par le programme
        if(octetRecu>=0):
            print(index,octetRecu.to_bytes(1, 'big'))
            simulArduino.write(b1)
            index+=1
            if(index==10) : simulArduino.write(b2)
            if(index==100) : break
