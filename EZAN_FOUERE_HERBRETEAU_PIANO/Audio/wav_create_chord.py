# -*- coding: utf-8 -*-
import sys
sys.path.append('../Sounds')
sys.path.append('..')
from wav_audio import *
from wav_create_notes_from_frequencies_db import *
from wave_generator import *

''' ouverture des fichiers des trois notes, et récupération de leur liste d'échantillons
Remarque : les trois sons doivent bien entendu avoir été créé avec la même fréquence d'échantillonnage... '''

def generate_chords(harmonics, t=1):
    print(harmonics)
    data=[]
    dataX=[]
    noteList = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    for noteSTR in harmonics:
        if (not os.path.isfile("Sounds/"+noteSTR+".wav") and t==1) or (not os.path.isfile("Sounds/"+noteSTR+"t"+str(t)+"s.wav") and t!=1):
            note = noteSTR[0]
            degree=""
            if noteSTR[1] == "#":
                note+="#"
                for i in range(2, len(noteSTR)):
                    degree+= noteSTR[i]
            else:
                for i in range(1, len(noteSTR)):
                    degree+= noteSTR[i]

            if note not in noteList:
                print("cette note n'est pas supportée: "+note+degree)
                return
            if int(degree)>11:
                print("cette note n'est pas supportée: "+note+degree)
                return
            if int(degree)<0:
                print("cette note n'est pas supportée: "+note+degree)
                return
            else:
                print("wait during the generation of octave "+str(degree))
                octave_min_max(int(degree), int(degree))
                generate_notes(t)

        if t==1:
            X, framerate = open_wav("Sounds/"+noteSTR+'.wav')
        else:
            X, framerate = open_wav("Sounds/"+noteSTR+"t"+str(t)+"s.wav")
        dataX.append(X)

    if len(dataX)!=0 :
        addition=0
        x = 0
        for i in range(len(dataX[0])):
            for j in range(len(harmonics)):
                addition += dataX[j][i]
            x=+1
            data.append(float(1.0/float(len(harmonics))*addition))

            addition=0
        if t==1:
            name= "Sounds/"+'x'.join(harmonics)+"chord.wav"
        else:
            name= "Sounds/"+'x'.join(harmonics)+"chordt"+str(t)+"s.wav"
        save_wav(name, data, framerate)
        subprocess.call(["aplay",name])




#accords=['C3','F3','G10']
#data = generate_chords(accords)
#subprocess.call(["aplay","")
