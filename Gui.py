import tkinter as tk
from tkinter import Tk,Scale,Label,Radiobutton,StringVar

class Gui():
    def __init__(self, master):
        self.master = master
        self.x = 0 # position horizontale du fou en nombre de pas
        self.y = 0 # position verticzle du fou en nombre de pas
        self.xMax = 10000 # valeur par défaut du nombre de pas à l'horizontale (réglé au final par le pilote)
        self.yMax = 5000 # valeur par défaut du nombre de pas à l'horizontale (réglé au final par le pilote)
        self.widthCanvas = 0 # largeur du canvas permettant l'affichage de la plaque de marbre
        self.heightCanvas = 0 # hauteur du canvas permettant l'affichage de la plaque de marbre
        master.title("FOU")

        def sel():
            id = int(v.get())
            self.pilote.comportement.setId(id)
            self.pilote.demarrage()
            if(id>0):
                scaleX.set(0)
                scaleY.set(0)

        v = StringVar(master, "0")
        values = {"Manuel" : "0","InitPos" : "1","Carré" : "2","Cercle" : "3","vagabond droit" : "4"}

        for (text, value) in values.items():
            Radiobutton(master, text = text, command=sel,variable = v,
                value = value, indicator = 0,
                background = "light blue").pack(side = tk.LEFT,anchor=tk.N)

        scaleX = Scale(master, variable=tk.DoubleVar(),resolution = 5,length=500,command=self.selX,from_=-2000,to=2000,orient=tk.HORIZONTAL)
        scaleY = Scale(master, variable=tk.DoubleVar(),resolution = 5,length=400,command=self.selY,from_=-2000,to=2000,orient=tk.VERTICAL)
        scaleX.pack(anchor=tk.N)
        scaleY.pack(anchor=tk.W,side = tk.LEFT)
        self.widthCanvas = 400*self.xMax/self.yMax
        self.heightCanvas = 400
        self.monCanvas = tk.Canvas(master, bg="white", height=self.heightCanvas, width=self.widthCanvas)
        self.monCanvas.pack()


    def selX(self,val):
       self.pilote.setVitesseX(int(val))

    def selY(self,val):
       self.pilote.setVitesseY(int(val))

    def setPilote(self,p):
        self.pilote = p
        self.xMax = self.pilote.widthFou
        self.yMax = self.pilote.heightFou
        self.x = self.pilote.xPos
        self.y = self.pilote.yPos

    def setX(self,x):
        self.x = x

    def setY(self,y):
        self.y = y

    def majCanvas(self):
        self.x = self.pilote.xPos
        self.y = self.pilote.yPos
        width = self.widthCanvas
        height = self.heightCanvas
        xAff = self.x*width/self.xMax
        yAff = self.y*height/self.yMax
        self.monCanvas.delete('lastPoint')
        self.monCanvas.delete('lastLineX')
        self.monCanvas.delete('lastLineY')
        self.monCanvas.delete('lastTextX')
        self.monCanvas.delete('lastTextY')
        self.monCanvas.create_oval(xAff-2,yAff-2,xAff+2,yAff+2,outline='red',fill='red',tags='lastPoint')
        self.monCanvas.create_line(xAff,0,xAff,height,width=1,dash=(4, 2),tags='lastLineX')
        self.monCanvas.create_line(0,yAff,width,yAff,width=1,dash=(4, 2),tags='lastLineY')
        self.monCanvas.create_text(xAff+3,10,text='x = ' + str(self.x),tags='lastTextX',anchor=tk.NW)
        self.monCanvas.create_text(10,yAff+3,text='y = ' + str(self.y),tags='lastTextY',anchor=tk.NW)
