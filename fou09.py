from tkinter import Tk

from Gui import Gui
from Pilote import Pilote
import time

pilote = Pilote()

root = Tk()
gui = Gui(root)
gui.setPilote(pilote)

while(1):
    pilote.majSerie()
    gui.majCanvas()
    root.update()
