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


def ajouterOctaveSuivante():
    max = 0
    for octave in piano.octaves:
        if octave.degree > max:
            max= octave.degree

    degree = max+1
    if degree > 11:
        print("on ne peux pas créer une octave plus élevée")
    else:
        piano.create_octave(piano.frame, degree)

def ajouterOctavePrecedente():
    min = 3
    for octave in piano.octaves:
        if octave.degree < min:
            min= octave.degree

    degree = min-1
    if degree < 0:
        print("on ne peux pas créer une octave plus faible")
    else:
        piano.create_octave(piano.frame, degree)



mw = tk.Tk()
mw.geometry("800x800")
mw.title("Leçon de Piano")
frame=tk.Frame(mw,borderwidth=5,width=360,height=300)

boutonOctavePrev = tk.Button(frame, text="ajouter octave",command=lambda :ajouterOctavePrecedente())
boutonOctavePrev.pack(side="left")

boutonOctaveNext = tk.Button(frame, text="ajouter octave",command=lambda :ajouterOctaveSuivante())
boutonOctaveNext.pack(side="right")

octaves=1
piano=Piano(frame,octaves)
view=View(frame)
view.grid(4)
view.packing()
view.update()

frameGenerator = tk.Frame(frame)
frameGenerator.pack(side="left")

list = tk.Listbox(frameGenerator)
list.pack()
notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
for note in notes:
    list.insert("end", note)

buttonAjouter = tk.Button(frameGenerator, text="")

frame.pack()



mw.mainloop()
