# -*- coding: utf-8 -*-

import sys
major=sys.version_info.major
minor=sys.version_info.minor
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
elif major==3 and minor==6 :
    import tkinter as tk
    from tkinter import filedialog
else :
    print("Your python version is : ",major,minor)
    print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog
from math import pi,sin
import collections
import subprocess
from observer import *
from piano import *
from signal_visualizer import *
from wave_generator import *



def alert_popup(title, message):
    root = tk.Tk()
    root.title(title)
    w = 200     # popup window width
    h = 200     # popup window height
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w)/2
    y = (sh - h)/2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    m = message
    m += '\n'
    w = tk.Label(root, text=m, width=120, height=10)
    w.pack()
    b = tk.Button(root, text="OK", command=root.destroy, width=10)
    b.pack()


class Combine(Observer):
    def __init__(self,parent):
        self.parent=parent
        self.frame=tk.Frame(mw,borderwidth=5,width=360,height=300)
        self.listFreq=listNotes()
        octaves=1
        self.piano=Piano(self.frame,octaves,self)
        self.lastKey=self.piano.lastKey
        boutonOctavePrev = tk.Button(self.frame, text="ajouter octave",command=lambda :self.piano.ajouterOctavePrecedente())
        boutonOctavePrev.pack(side="left")
        boutonOctaveNext = tk.Button(self.frame, text="ajouter octave",command=lambda :self.piano.ajouterOctaveSuivante())
        boutonOctaveNext.pack(side="right")


        frameGenerator = tk.Frame(self.frame)
        frameGenerator.pack(side="left")
        viewGenerator = ViewGenerator(frameGenerator)





        self.view=View(self.frame)
        self.view.grid(4)
        self.view.packing()
        self.view.update()
        self.view.update(0)


        self.frame.pack(expand=1,fill="both")

    def updateSignal(self,piano):
        self.lastKey=piano.lastKey
        if self.lastKey[1]=='#':
            self.lastKey=self.lastKey[0]+"sharp"+self.lastKey[2]
        freq=self.listFreq.get(self.lastKey)
        self.view.update(freq)

    def updateList(self):
        self.listFreq.update(listNotes())








if __name__=="__main__":
    mw = tk.Tk()
    mw.geometry("800x800")
    mw.title("Leçon de Piano")
    c=Combine(mw)
    group="Charles EZAN \nAlexandre FOUERE \nGuillaume Herbreteau"
    menubar = tk.Menu(mw)
    mw.config(menu=menubar)
    menufichier = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Fichier", menu=menufichier)
    menufichier.add_command(label="Quitter", command = mw.destroy)
    menuhelp = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=menuhelp)
    menuhelp.add_command(label="Membres du groupe", command=lambda: alert_popup("Membres du groupe",group))



    mw.mainloop()
