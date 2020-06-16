# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/34522095/gui-button-hold-down-tkinter


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
    print("wait during the generation of octave "+str(min)+" to "+str(max))
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
        txt= "Pour créer un accord, tapez dans la ligne de saisie une note suivie d'une octave\n Les notes sont les suivantes\n"+"C, C#, D, D#, E, F, F#, G, G#, A, A#, B\n"+"Et les octaves peuvent être choisies de 0 à 11\n exemple de note: C#3"
        label = tk.Label(self.parent, text=txt)
        label.pack()
        framelist = tk.Frame(parent)
        self.list=tk.Listbox(framelist)
        self.list.configure(height=4)
        self.list.pack(side="left")

        texte = tk.Label(framelist, text="Liste des notes pour créer l'accord. Sélectionnez et appuyez sur suppr pour supprimer une note de la liste", wraplength="300", width="40")
        texte.pack(side="left")

        framelist.pack()

        frameEntry = tk.Frame(parent)
        self.entry=tk.Entry(frameEntry)
        self.entry.pack(side="left")

        texte1 = tk.Label(frameEntry, text="Saisissez une note puis validez avec entrée", wraplength="300", width="40")
        texte1.pack(side="left")

        frameEntry.pack()

        modelList = ModelList([])
        self.update(modelList)
        modelList.attach(self)
        controllerList = ControllerList(modelList,self)

        slider = tk.Scale(parent, orient = 'horizontal', from_ = 1, to = 9, resolution = 1,
                        tickinterval = 2, length = 250, label = "Durée de l'accord")
        slider.set(1)
        slider.pack(pady="20")

        button = tk.Button(parent, text="enregistrer l'accord et le jouer",command=lambda :generate_chords(modelList.get_data(),slider.get()))
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
    mw.geometry("500x300")
    mw.title("Generateur de fichier au format WAV")

    viewGenerator = ViewGenerator(mw)



    mw.mainloop()
