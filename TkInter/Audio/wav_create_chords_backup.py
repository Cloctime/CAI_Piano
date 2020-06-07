# -*- coding: utf-8 -*-
import sys
sys.path.append('../Sounds')
sys.path.append('..')
from wav_audio import *
from wav_create_notes_from_frequencies_db import *
from wave_generator import *

''' ouverture des fichiers des trois notes, et récupération de leur liste d'échantillons
Remarque : les trois sons doivent bien entendu avoir été créé avec la même fréquence d'échantillonnage... '''

def generate_chords(harmonics):
    print(harmonics)
    data=[]
    dataX=[]
    noteList = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    for noteSTR in harmonics:
        if not os.path.isfile("../Sounds/"+noteSTR+".wav"):
            note = noteSTR[0]
            degree=""
            if noteSTR[1] == "#":
                note+="#"
                for i in range(2, len(noteSTR)):
                    degree+= noteSTR[i]
            else:
                for i in range(1, len(noteSTR)):
                    degree+= noteSTR[i]

            print(note)
            print(degree)

            if note not in noteList:
                print("cette note n'est pas supportée: "+note)
            else:
                generateOctaves(int(degree),int(degree))

        X, framerate = open_wav("../Sounds/"+noteSTR+'.wav')
        dataX.append(X)
    addition=0
    x = 0
    for i in range(len(dataX[0])):
        for j in range(len(harmonics)):
            addition += dataX[j][i]
        x=+1
        data.append((1/len(harmonics)*addition))
        addition=0
    name= "../Sounds/"+'x'.join(harmonics)+".wav"
    save_wav(name, data, framerate)




accords=['C3','F3','G10']
data = generate_chords(accords)
#subprocess.call(["aplay","")
