import numpy as np
import math

def calcNPas(v):
    redPas = calcRedPas(v)
    if(v<0) : redPas = -redPas
    if(v==0) : redPas =0
    return redPas

def calcRedPas(v):
    v = int(abs(v))
    redPasLin = 0.00185*v + 0.03
    redPas = 1/2**math.ceil(math.log2(1/redPasLin))
    return redPas

def setAmaxXY(res,aMax,vX,oldVX,vY,oldVY):
    # détermination des accélérations max aX et aY à partir des anciennes valeurs de v
    if(vX==0 and vY ==0) :
        v = np.sqrt(oldVX*oldVX + oldVY*oldVY)
        aX = aMax*abs(oldVX)/ v
        aY = aMax*abs(oldVY)/ v
    else :
        v = np.sqrt(vX*vX + vY*vY)
        aX = aMax*abs(vX)/v
        aY = aMax*abs(vY)/v
    if(vX<oldVX) : aX = -aX
    if(vY<oldVY) : aY = -aY

    # calcul d'une approximation de vX et vY surévaluée
    # objectif : calcul du taux de réduction des pas : redPasX et redPasY
    delta =(abs(oldVX) + 0.00185*aX*res)**2 + 4*0.03*aX*res
    if(delta>=0):
        approxVX = (abs(oldVX) + 0.00185*aX*res + math.sqrt(delta))/2
    else : approxVX = 0
    redPasX = calcRedPas(approxVX)

    delta =(abs(oldVY) + 0.00185*aY*res)**2 + 4*0.03*aY*res
    if(delta>=0):
        approxVY = (abs(oldVY) + 0.00185*aY*res + math.sqrt(delta))/2
    else : approxVY = 0
    redPasY = calcRedPas(approxVY)

    # calcul des accélérations à partir de vX et vY souhaité
    if(vX==0) : aX_voulu = -oldVX*oldVX/(redPasX*res)
    else : aX_voulu = (vX - oldVX)*vX/(redPasX*res)
    if(vY==0) : aY_voulu = -oldVY*oldVY/(redPasY*res)
    else : aY_voulu = (vY - oldVY)*vY/(redPasY*res)
    a_voulu = np.sqrt(aX_voulu*aX_voulu + aY_voulu*aY_voulu)

    # si l'accélération souhaitée dépasse la valeur max, il faut agir et calculer vX et vY
    if(a_voulu>aMax):
        aX = aX_voulu*aMax/a_voulu # aX au max
        deltaX = oldVX*oldVX + 4*aX*redPasX*res
        if(deltaX>=0):
            vv = vX
            if(vX==0):vv=oldVX
            if(vv>0) :
                vX=(oldVX + np.sqrt(deltaX))/2
            else : vX=(oldVX - np.sqrt(deltaX))/2
        else : vX = 0

        aY = aY_voulu*aMax/a_voulu # aY au max
        deltaY = oldVY*oldVY + 4*aY*redPasY*res
        if(deltaY>=0):
            vv = vY
            if(vY==0):vv=oldVY
            if(vv>0) :
                vY=(oldVY + np.sqrt(deltaY))/2
            else : vY=(oldVY - np.sqrt(deltaY))/2
        else : vY = 0

    return vX,vY


class Goto():
    def __init__(self,res):
        self.resolution = res
        self.xPos0 = 0
        self.yPos0 = 0
        self.init()

    def setParam(self,aMax,vMax,xCible,yCible):
        self.aMax = aMax
        self.vMax = vMax
        self.xCible = xCible
        self.yCible = yCible

    def init(self):
        self.phase = -1
        self.dAccel = 0
        self.index=0

    def maj(self,vX_old,vY_old,xPos,yPos) :
        if(self.phase==-1):# phase d'initialisation
            self.xPos0 = xPos
            self.yPos0 = yPos
            print("phaseAccel")
            self.phase = 0

        #calcul de la distance parcourue
        dx = xPos - self.xPos0
        dy = yPos - self.yPos0
        d0 = np.sqrt(dx*dx + dy*dy)

        #calcul de la distance jusqu'à la cible
        dx = self.xCible - xPos
        dy = self.yCible - yPos
        dCible = np.sqrt(dx*dx+dy*dy)

        # calcul des vitesses
        if(dCible == 0) : return 0,0
        vX = self.vMax * dx / dCible
        vY = self.vMax * dy / dCible

        if(self.phase == 0): # phase d'accélération
            oldV = np.sqrt(vX_old*vX_old+vY_old*vY_old)
            v = np.sqrt(vX*vX+vY*vY)
            dx = calcNPas(vX)*self.resolution
            dy = calcNPas(vY)*self.resolution
            dPas = np.sqrt(dx*dx+dy*dy)
            if (abs(v-oldV)<0.01*self.vMax) : # on a atteint la vitesse maximale à 1% près
                self.dAccel = d0 - dPas # distance parcourue pendant la phase d'accélération
                print("phase vit constante")
                self.phase = 1

            if (dCible<=d0-dPas): # la moitié de la distance a été parcourue, on décélère
                print("phaseDecel")
                self.phase = 2

            vX,vY = setAmaxXY(self.resolution,self.aMax,vX,vX_old,vY,vY_old)
            if(vX>0 and vX<25) : vX = 25
            if(vX<0 and vX>-25) : vX = -25
            if(vY>0 and vY<25) : vY = 25
            if(vY<0 and vY>-25) : vY = -25

        if(self.phase == 1 ) : # phase de vitesse constante
            if(dCible<self.dAccel) :
                self.phase = 2
                self.dAccel = 0
                print("phaseDecel")
            #vX,vY = setAmaxXY(self.resolution,self.aMax,vX,vX_old,vY,vY_old)

        if(self.phase==2): # phase de décélération
            vMin = 50
            vX,vY = setAmaxXY(self.resolution,self.aMax,0,vX_old,0,vY_old)
            if(vX>0 and vX<vMin) : vX = vMin
            if(vX<0 and vX>-vMin) : vX = -vMin
            if(vY>0 and vY<vMin) : vY = vMin
            if(vY<0 and vY>-vMin) : vY = -vMin
            # en fin de parcours, on ajuste précisément pour tomber exactement sur la cible

            grainX = calcNPas(vX)*self.resolution
            grainY = calcNPas(vY)*self.resolution
            xPosPrevu = xPos+grainX
            yPosPrevu = yPos+grainY

            if(grainX == 0) : grainX = calcNPas(vMin)*self.resolution
            if(grainY == 0) : grainY = calcNPas(vMin)*self.resolution
            if(xPos<self.xCible+grainX and xPos>self.xCible-grainX): vX = 0
            elif(vX>0 and xPosPrevu>self.xCible): vX = vMin
            elif(vX<0 and xPosPrevu<self.xCible): vX = -vMin
            elif(vX == 0 and xPosPrevu<self.xCible) : vX = vMin
            elif(vX == 0 and xPosPrevu>self.xCible) : vX = -vMin

            if(yPos<self.yCible+grainY and yPos>self.yCible-grainY) : vY = 0
            elif(vY>0 and yPosPrevu>self.yCible): vY = vMin
            elif(vY<0 and yPosPrevu<self.yCible): vY = -vMin
            elif(vY == 0 and yPosPrevu<self.yCible) : vY = vMin
            elif(vY == 0 and yPosPrevu>self.yCible) : vY = -vMin

        if(vX==0 and vY==0) : self.phase = 3
        self.index +=1
        return vX,vY

# test unitaire méthode GOTO
import msvcrt
if __name__ == '__main__':
    goto = Goto(10)
    goto.setParam(1000,500,1000,0) # aMax,vMax,xCible,yCible
    xPos = 0
    yPos = 0
    vX_old = 0
    vY_old = 0
    t=0
    tempStr = ""

    while(1) :
        vX,vY = goto.maj(vX_old,vY_old,xPos,yPos)
        if(vX == 0  and vY == 0) : break

        if(vX != 0):
            dX = calcNPas(vX)*10
            aX = (vX-vX_old)*vX/dX
            xPos += dX
            vX_old = vX
            print("X : nPasX = " + str(dX),
                "xPos = " + str(int(xPos)),
                "vX = " + str(int(vX)),
                "aX = " + str(int(aX))
            )

        if(vY != 0):
            dY = calcNPas(vY)*10
            aY = (vY-vY_old)*vY/dY
            yPos += dY
            vY_old = vY
            print("Y : nPasY = " + str(dY),
                "yPos = " + str(int(yPos)),
                "vY = " + str(int(vY)),
                "aY = " + str(int(aY))
            )

        print("-------------------------------------")

        if (vX == 0) : dt = 0
        else : dt = dX/vX
        t+=dt
        tempStr += (str(t) + ";"
                + str(xPos) + ";"
                + str(vX) + "\n")

    with open('data.csv', 'w') as output:
         output.write(tempStr)

    import matplotlib.pyplot as plt
    import csv
    x = []
    y = []

    with open('data.csv','r') as csvfile:
        lines = csv.reader(csvfile, delimiter=';')
        for row in lines:
            x.append(float(row[0]))
            y.append(float(row[2]))

    plt.plot(x,y)
    plt.xlabel('t')
    plt.ylabel('vX')
    plt.title('vX en fonction de t')
    plt.show()
