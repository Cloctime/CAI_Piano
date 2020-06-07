# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/34522095/gui-button-hold-down-tkinter

#coucou

import sys
import math

sys.path.append('Audio')
from frequencies import octave_min_max
from wav_create_notes_from_frequencies_db import generate_notes
from wav_create_chord import *


def generateOctaves(min, max):
    if min<0:
        min=0
    if max>11:
        max = 11
    octave_min_max(min, max)
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



class ModelList():
    def __init__(self, names=[]):
        self.__data = names
        self.observers= []
    def get_data(self):
        return self.__data
    def notify(self):
        for obs in self.observers:
            obs.update(self)
    def insert(self,name):
        self.__data.append(name)
        self.notify()
    def delete(self, index):
        del self.__data[index]
        self.notify()
    def attach(self, obs):
        if not hasattr(obs,"update"):
            raise ValueError("Observer must have \
                        an update() method")
        self.observers.append(obs)
    def detach(self, obs):
        if obs in self.observers :
            self.observers.remove(obs)


class ViewGenerator():
    def __init__(self,parent):
        self.parent=parent
        self.list=tk.Listbox(parent)
        self.list.configure(height=4)
        self.list.pack()
        self.entry=tk.Entry(parent)
        self.entry.pack()
        modelList = ModelList([])
        self.update(modelList)
        modelList.attach(self)
        controllerList = ControllerList(modelList,self)

        button = tk.Button(parent, text="enregistrer l'accord",command=lambda :generate_chords(modelList.get_data()))
        button.pack()
    def update(self,model):
        self.list.delete(0, "end")
        for data in model.get_data():
            self.list.insert("end", data)

class ControllerList():
    def __init__(self,model,view):
        self.model,self.view = model,view
        self.view.entry.bind("<Return>",
        self.enter_action)
        self.view.list.bind("<Delete>",
        self.delete_action)
    def enter_action(self, event):
        data = self.view.entry.get()
        self.model.insert(data)
    def delete_action(self, event):
        for index in self.view.list.curselection():
            self.model.delete(int(index))

if __name__ == "__main__" :
    mw = tk.Tk()
    mw.geometry("360x300")
    mw.title("Generateur de fichier au format WAV")

    notes=[]
    modelList = ModelList(notes)
    viewList = ViewList(mw)
    viewList.update(modelList)
    modelList.attach(viewList)
    controllerList = ControllerList(modelList,viewList)

    button = tk.Button(mw, text="enregistrer l'accord",command=lambda :generate_chords(modelList.get_data()))
    button.pack()



    mw.mainloop()
