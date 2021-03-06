# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/34522095/gui-button-hold-down-tkinter

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
    if __name__ == "__main__" :
        print("Your python version is : ",major,minor)
        print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog
from math import pi,sin
import collections
import subprocess
from observer import *
from wave_generator import generateOctaves


class Piano() :
    def __init__(self,parent,octaves,obs=0) :
        self.parent=parent
        self.octaves=[]
        self.frame1=tk.LabelFrame(self.parent,bg="yellow", text="Piano")
        boutonOctavePrev = tk.Button(self.frame1, text="ajouter octave",command=lambda :self.ajouterOctavePrecedente())
        boutonOctavePrev.pack(side="left")
        boutonOctaveNext = tk.Button(self.frame1, text="ajouter octave",command=lambda :self.ajouterOctaveSuivante())
        boutonOctaveNext.pack(side="right")

        self.frame1.pack(expand="1")

        self.frame=tk.Frame(self.frame1,bg="yellow")

        self.obs=obs
        for octave in range(octaves) :
            self.create_octave(self.frame,octave+2)
        self.frame.pack(fill="x", expand="1")

        self.lastKey=None


    def notify(self):
        self.obs.updateSignal(self)

    def create_octave(self,parent,degree=3) :
        model=Octave(degree)
        control=Keyboard(parent,model,self,degree)
        view=Screen(parent)
        model.attach(view)
        control.get_keyboard().grid(column=degree,row=0)
        view.get_screen().grid(column=degree,row=1)
        self.octaves.append(model)
        generateOctaves(degree,degree)
        if self.obs!=0:
            self.obs.updateList()



    def ajouterOctaveSuivante(self):
        max = 0
        for octave in self.octaves:
            if octave.degree > max:
                max= octave.degree

        degree = max+1
        if degree > 11:
            print("on ne peux pas créer une octave plus élevée")
        else:
            self.create_octave(self.frame, degree)

    def ajouterOctavePrecedente(self):
        min = 3
        for octave in self.octaves:
            if octave.degree < min:
                min= octave.degree

        degree = min-1
        if degree < 0:
            print("on ne peux pas créer une octave plus faible")
        else:
            self.create_octave(self.frame, degree)

class Octave(Subject) :
    def __init__(self,degree=3) :
        Subject.__init__(self)
        self.degree=degree
        self.set_sounds_to_gamme(degree)
    def get_gamme(self) :
        return self.gamme
    def set_gamme(self,gamme) :
        self.gamme=gamme
    def get_degree(self) :
        return self.degree
    def notify(self,key) :
        for obs in self.observers:
            obs.update(self,key)

    def set_sounds_to_gamme(self,degree=3) :
        self.degree=degree
        folder="Sounds"
        notes=["C","D","E","F","G","A","B","C#","D#","F#","G#","A#"]
        self.gamme=collections.OrderedDict()
        for key in notes :
            self.gamme[key]="Sounds/"+key+str(degree)+".wav"
        return self.gamme

class Screen(Observer):
    def __init__(self,parent) :
        self.parent=parent
        self.create_screen()
    def create_screen(self) :
        self.screen=tk.Frame(self.parent,borderwidth=5,width=500,height=160,bg="pink")
        self.info=tk.Label(self.screen,text="Appuyez sur une touche clavier ",bg="pink",font=('Arial',10))
        self.info.pack()
    def get_screen(self) :
        return self.screen
    def update(self,model,key="C") :
        if __debug__:
            if key not in model.gamme.keys() :
                raise AssertionError
        subprocess.call(["aplay",model.get_gamme()[key]])
        if self.info :
            self.info.config(text="Vous avez joue la note: "+ key + str(model.get_degree()))


class Keyboard :
    def __init__(self,parent,model,piano,degree) :
        self.parent=parent
        self.model=model
        self.piano=piano
        self.degree=degree
        self.create_keyboard()
    def create_keyboard(self) :
        key_w,key_h=40,150
        dx_white,dx_black=0,0
        self.keyboard=tk.Frame(self.parent,borderwidth=5, width=7*key_w,height=key_h,bg="red")
        for key in self.model.gamme.keys() :
            if key.startswith('#',1,len(key)) :
                delta_w,delta_h=3/4.,2/3.
                delta_x=3/5.
                button=tk.Button(self.keyboard,name=key.lower(),width=3,height=6,bg="black")
                button.bind("<Button-1>",lambda event,x=key : self.defineLastKey(x))


                button.place(width=key_w*delta_w,height=key_h*delta_h,x=key_w*delta_x+key_w*dx_black,y=0)
                if key.startswith('D#', 0, len(key) ) :
                    dx_black=dx_black+2
                else :
                    dx_black=dx_black+1
            else :
                button=tk.Button(self.keyboard,name=key.lower(),bg = "white")

                button.bind("<Button-1>",lambda event,x=key : self.defineLastKey(x))


                button.place(width=key_w,height=key_h,x=key_w*dx_white,y=0)
                dx_white=dx_white+1

    def play_note(self,key) :
        self.model.notify(key)
    def get_keyboard(self) :
        return self.keyboard
    def get_degrees(self) :
        return self.degrees

    def defineLastKey(self,key):
        self.piano.lastKey=key+str(self.degree)
        self.play_note(key)
        #subprocess.call(["aplay","Sounds/"+key+str(self.degree)+".wav"])
        if self.piano.obs!=0:
            self.piano.notify()







if __name__ == "__main__" :
    mw = tk.Tk()
    mw.geometry("800x300")
    octaves=2
    mw.title("La leçon de piano à " + str(octaves) + " octaves")
    piano=Piano(mw,octaves)
    mw.mainloop()
