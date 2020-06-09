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




class Combine(Observer):
    def __init__(self,parent):
        self.parent=parent
        self.frame=tk.Frame(mw,borderwidth=5,width=360,height=300)
        octaves=1
        self.piano=Piano(self.frame,octaves,self)
        self.lastKey=self.piano.lastKey
        boutonOctavePrev = tk.Button(self.frame, text="ajouter octave",command=lambda :self.piano.ajouterOctavePrecedente())
        boutonOctavePrev.pack(side="left")
        boutonOctaveNext = tk.Button(self.frame, text="ajouter octave",command=lambda :self.piano.ajouterOctaveSuivante())
        boutonOctaveNext.pack(side="right")
        frameGenerator = tk.Frame(self.frame)
        frameGenerator.pack(side="left")
        list = tk.Listbox(frameGenerator)
        list.pack()
        notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        for note in notes:
            list.insert("end", note)

        self.listFreq=listNotes()
        print(self.listFreq)




        self.view=View(self.frame)
        self.view.grid(4)
        self.view.packing()
        self.view.update()

        self.view.update(0)

        self.frame.pack()

    def update(self,piano):
        self.lastKey=piano.lastKey
        if self.lastKey[1]=='#':
            self.lastKey=self.lastKey[0]+"sharp"+self.lastKey[2]
        freq=self.listFreq.get(self.lastKey)
        print("freq:",freq)
        self.listFreq=listNotes()
        self.view.update(freq)







if __name__=="__main__":
    mw = tk.Tk()
    mw.geometry("800x800")
    mw.title("Leçon de Piano")
    c=Combine(mw)



    mw.mainloop()
