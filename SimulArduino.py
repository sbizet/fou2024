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
        self.widthFou = 10000 # nombre de pas total à l'horizontale ... à déterminer
        self.heightFou = 5000 # nombre de pas total à la verticale ... à déterminer
        self.xPos = 500 # à changer
        self.yPos = 100 # à changer
        self.redPasX = 0
        self.redPasY = 0
        self.codeFc = 0

    def write(self,b):
        x_ou_y = (b[0] >> 7) & 1
        nTop = 0
        nTop |= ((b[0] >> 1) & 1)<<7
        nTop |= ((b[0] >> 0) & 1)<<6
        for i in range(6):
            nTop |= ((b[1] >> i) & 1)<<i

        codePas = 0
        codePas |= ((b[0] >> 2) & 1)<<2
        codePas |= ((b[0] >> 3) & 1)<<1
        codePas |= ((b[0] >> 4) & 1)<<0
        if (codePas>3) : codePas = 4

        dir = (((b[0] >> 5) & 1)-0.5)*2
        if(x_ou_y == 0) :
            self.nTopX = nTop
            self.redPasX = dir/(2**codePas)
        else :
            self.nTopY = nTop
            self.redPasY = dir/(2**codePas)

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
                self.xPos += self.redPasX*self.resolution
                self.octetEnvoi = 0 + self.codeFc
            elif(maintenant-self.toX>self.dtX):
                self.toX = self.toX+self.dtX
                self.xPos += self.redPasX*self.resolution
                self.octetEnvoi = 0 + self.codeFc

        if(self.dtY>0):
            if(maintenant-self.toY>2*self.dtY):
                self.toY = maintenant
                self.yPos += self.redPasY*self.resolution
                self.octetEnvoi = 128 + self.codeFc # ou 0 ??
            elif(maintenant-self.toY>self.dtY and self.octetEnvoi == -1):
                self.toY = self.toY+self.dtY
                self.yPos += self.redPasY*self.resolution
                self.octetEnvoi = 128 + self.codeFc

        self.codeFc = 0
        if(self.xPos<=0) : self.codeFc |= (1<<0)
        if(self.xPos>=self.widthFou) : self.codeFc |= (1<<1)
        if(self.yPos<=0) : self.codeFc |= (1<<2)
        if(self.yPos>=self.heightFou) : self.codeFc |= (1<<3)

# testUnitaire
if __name__ == '__main__':
    import time
    simulArduino = SimulArduino()
    b1 = bytearray([57,100]) # sur X : 57 = 0011 1001 et 100 = 0110 0100 -> nTop = 100 ; redPas = 1/8; dir > 0
    b2 = bytearray([177,203]) # sur Y : 177 = 1011 0001 et 203 = 1100 1011 -> nTop = 75 ; redPas = 1/2; dir > 0
    simulArduino.write(b1) # envoyé à l'Arduino simulée par le programme
    index = 0
    to = time.time()

    while (1) :
        simulArduino.timer()
        octetRecu = simulArduino.read() # envoyé par Arduino simulée, lu par le programme
        if(octetRecu>=0):
            print(time.time()-to,index,octetRecu.to_bytes(1, 'big'),simulArduino.xPos,simulArduino.yPos)
            index+=1
            if(index==100) : simulArduino.write(b2) # pour piloter l'axe y ...
            if(index==200) : break
