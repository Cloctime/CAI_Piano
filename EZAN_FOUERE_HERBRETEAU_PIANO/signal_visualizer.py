# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/34522095/gui-button-hold-down-tkinter

import sys
import sqlite3
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
from math import pi,sin,cos



class View :
    def __init__(self,parent,bg="white",width=600,height=300):
        self.canvas=tk.Canvas(parent,bg=bg,width=width,height=height)
        self.a,self.f,self.p=1.0,1.0,0.0
        self.signal=[]
        self.width,self.height=width,height
        self.units=1
        self.canvas.bind("<Configure>",self.resize)
        self.signal_id=0
        self.update(self.f)



    def vibration(self,t,harmoniques=1,impair=True):
        a,f,p=self.a,self.f,self.p
        somme=0
        for h in range(1,harmoniques+1) :

            somme=somme + (a/h)*sin(2*pi*(f*h)*t-p)
        return somme

    def generate_signal(self,period=2,samples=100.0):
        del self.signal[0:]
        echantillons=range(int(samples)+1)
        Tech = period/samples
        for t in echantillons :
            self.signal.append([t*Tech,self.vibration(t*Tech)])
        return self.signal

    def update(self,frequency=1,amplitude=1,phase=0):
        print("View : update()")
        self.f=frequency
        self.a=amplitude
        self.p=phase
        self.generate_signal()

        if self.signal :
            self.plot_signal(self.signal)

    def plot_signal(self,signal,color="red"):

        self.canvas.delete(self.signal_id)

        w,h=self.width,self.height
        signal_id=None
        if signal and len(signal) > 1:
            plot = [(x*w,h/2.0*(1-y*1.0/(self.units/2.0))) for (x, y) in signal]
            self.signal_id=self.canvas.create_line(plot, fill=color, smooth=1, width=3,tags="sound")
        return self.signal_id

    def grid(self,steps=2):
        self.units=steps
        tile_x=self.width/steps
        for t in range(1,steps+1):
            x =t*tile_x
            self.canvas.create_line(x,0,x,self.height,tags="grid")
            self.canvas.create_line(x,self.height/2-10,x,self.height/2+10,width=3,tags="grid")
        tile_y=self.height/steps
        for t in range(1,steps+1):
            y =t*tile_y
            self.canvas.create_line(0,y,self.width,y,tags="grid")
            self.canvas.create_line(self.width/2-10,y,self.width/2+10,y,width=3,tags="grid")

    def resize(self,event):
        if event:
            self.width,self.height=event.width,event.height
            self.canvas.delete("grid")
            self.canvas.delete("sound")
            self.plot_signal(self.signal)
            self.grid(self.units)

    def packing(self) :
        self.canvas.pack(expand=1,fill="both",padx=6)




def listNotes():
    connect = sqlite3.connect("Audio/frequencies.db")
    cursor = connect.cursor()

    temp=cursor.execute("SELECT octave FROM frequencies")
    octaves=[]
    for t in temp:
        octaves.append(t[0])
    notes={}

    for o in octaves:
        no=str(o)
        cursor.execute("SELECT C FROM frequencies where octave = ?", no)
        notes["C{0}".format(o)]=cursor.fetchone()[0]
        cursor.execute("SELECT Csharp FROM frequencies where octave = ?", no)
        notes["Csharp{0}".format(o)] = cursor.fetchone()[0]
        cursor.execute("SELECT D FROM frequencies where octave = ?", no)
        notes["D{0}".format(o)] = cursor.fetchone()[0]
        cursor.execute("SELECT Dsharp FROM frequencies where octave = ?", no)
        notes["Dsharp{0}".format(o)] = cursor.fetchone()[0]
        cursor.execute("SELECT E FROM frequencies where octave = ?", no)
        notes["E{0}".format(o)] = cursor.fetchone()[0]
        cursor.execute("SELECT F FROM frequencies where octave = ?", no)
        notes["F{0}".format(o)] = cursor.fetchone()[0]
        cursor.execute("SELECT Fsharp FROM frequencies where octave = ?", no)
        notes["Fsharp{0}".format(o)]=cursor.fetchone()[0]
        cursor.execute("SELECT G FROM frequencies where octave = ?", no)
        notes["G{0}".format(o)] = cursor.fetchone()[0]
        cursor.execute("SELECT Gsharp FROM frequencies where octave = ?", no)
        notes["Gsharp{0}".format(o)] = cursor.fetchone()[0]
        cursor.execute("SELECT A FROM frequencies where octave = ?", no)
        notes["A{0}".format(o)] = cursor.fetchone()[0]
        cursor.execute("SELECT Asharp FROM frequencies where octave = ?", no)
        notes["Asharp{0}".format(o)] = cursor.fetchone()[0]
        cursor.execute("SELECT B FROM frequencies where octave = ?", no)
        notes["B{0}".format(o)] = cursor.fetchone()[0]

    return notes





class ListApp(tk.Tk):
    def __init__(self,parent):
        self.parent=parent
        self.list_frame=tk.LabelFrame(self.parent,borderwidth=5,width=360,height=300)
        self.list = tk.Listbox(self.list_frame)
        self.list.pack()
        self.notes=listNotes()
        self.list.insert(0, *listNotes())
        self.print_btn = tk.Button(self.list_frame, text="Afficher note",
                                   command=self.print_selection)



        self.parent=parent

        self.frame=tk.LabelFrame(self.parent,borderwidth=5,width=360,height=300)
        self.frame.pack()
        self.view=View(self.frame)
        self.view.grid(4)
        self.view.packing()
        self.list_frame.pack(side='left',padx=30)
        self.print_btn.pack(fill=tk.BOTH)


        self.slider_frame=tk.LabelFrame(self.parent,borderwidth=5,width=360,height=300)

        slider_frequency = tk.Scale(self.slider_frame, orient = 'horizontal', from_ = 0, to = 15, resolution = 1,
                        tickinterval = 5, length = 250, label = "Fréquence")
        slider_frequency.set(1)
        slider_frequency.pack(pady="20")

        slider_magnitude = tk.Scale(self.slider_frame, orient = 'horizontal', from_ = 0, to = 2, resolution = 0.1,
                        tickinterval = 1, length = 250, label = "Amplitude")
        slider_magnitude.set(1)
        slider_magnitude.pack(pady="20")

        slider_phase = tk.Scale(self.slider_frame, orient = 'horizontal', from_ = -180, to = 180, resolution = 1,
                        tickinterval = 90, length = 250, label = "Phase")
        slider_phase.set(0)
        slider_phase.pack(pady="20")

        button_draw = tk.Button(self.slider_frame, text="Dessiner signal",command=lambda :self.view.update(slider_frequency.get(),slider_magnitude.get(),slider_phase.get()))
        button_draw.pack()

        self.slider_frame.pack(side='right',padx=30)
    def print_selection(self):

        selection = self.list.curselection()
        selec=[self.list.get(i) for i in selection][0]
        freq=self.notes.get(selec)

        self.view.update(freq)



if __name__ == "__main__" :
    mw = tk.Tk()
    mw.geometry("530x700")
    mw.title("Visualisation de signal sonore")

    list=ListApp(mw)




    mw.mainloop()
