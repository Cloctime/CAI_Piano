# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/34522095/gui-button-hold-down-tkinter

#coucou

import sys
import math

sys.path.append('Audio')
from frequencies import octave_min_max
from wav_create_notes_from_frequencies_db import generate_notes


def generateOctaves():
    octave_min_max(2,3)
    generate_notes()


def fetchEntry(button):
    if type(button.get()) is float or int:
        print(type(button.get()))
        result= round(float(button.get()))
        print(result)
        return result
    else :
        return 0




major=sys.version_info.major
minor=sys.version_info.minor
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
elif major==3 and minor==6 :
    import tkinter as tk
    from tkinter import filedialog
else :
    if __name__ == "__main__" :
        print("Your python version is : ",major,minor)
        print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog

if __name__ == "__main__" :
    mw = tk.Tk()
    mw.geometry("360x300")
    mw.title("Generateur de fichier au format WAV")
    frame=tk.Frame(mw,borderwidth=5,width=360,height=300,bg="pink")

    tk.Label(mw, text="First Name")
    tk.Label(mw, text="Last Name")

    e1 = tk.Entry(mw)
    e2 = tk.Entry(mw)


    boutonGenerate = tk.Button(frame, text="generate octaves",command=lambda :generateOctaves())   #lambda pour éviter d'appeler dès l'exécution !!!
    boutontest = tk.Button(frame, text="test",command=lambda :print(type(fetchEntry(e1))))
    frame.pack()
    boutonGenerate.pack()
    boutontest.pack()
    e1.pack()
    mw.mainloop()
