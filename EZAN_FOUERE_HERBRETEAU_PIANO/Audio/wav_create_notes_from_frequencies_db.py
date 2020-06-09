# -*- coding: utf-8 -*-
# script wav_audio.py
#http://fsincere.free.fr/isn/python/cours_python_ch9.php
#http://izeunetit.fr/ICN1ere/son_audio.php
# (C) Fabrice Sincère ; Jean-Claude Meilland
import wave
import math
import sqlite3

import os
import shutil


## Création d'un fichier audio au format WAV (PCM 8 bits stéréo 44100 Hz)
## Son de forme sinusoïdale sur chaque canal

def create_note_wav(degree,name,left_frequency,right_frequency,t=1) :
    if type(degree) != str :
        degree=str(degree)
    if t==1:
        file= name+degree+".wav"
    else:
        file= name+degree+"t"+str(t)+"s.wav"

    sound=wave.open("Sounds/"+file,'w')
    nb_channels = 2    # stéreo
    nb_bytes = 1       # taille d'un échantillon : 1 octet = 8 bits
    sampling = 44100   # fréquence d'échantillonnage
    left_level = 1    # niveau canal de gauche (0 à 1) ? '))
    right_level= 0.5    # niveau canal de droite (0 à 1) ? '))
    duration = t
    nb_samples = int(duration*sampling)
    params = (nb_channels,nb_bytes,sampling,nb_samples,'NONE','not compressed')
    sound.setparams(params)    # création de l'en-tête (44 octets)

    # niveau max dans l'onde positive : +1 -> 255 (0xFF)
    # niveau max dans l'onde négative : -1 ->   0 (0x00)
    # niveau sonore nul :                0 -> 127.5 (0x80 en valeur arrondi)

    left_magnitude = 127.5*left_level
    right_magnitude= 127.5*right_level

    for i in range(0,nb_samples):
        # canal gauche
        # 127.5 + 0.5 pour arrondir à l'entier le plus proche
        left_value = wave.struct.pack('B',int(128.0 + left_magnitude*math.sin(2.0*math.pi*left_frequency*i/sampling)))
        # canal droit
        right_value = wave.struct.pack('B',int(128.0 + right_magnitude*math.sin(2.0*math.pi*right_frequency*i/sampling)))
        sound.writeframes(left_value + right_value) # écriture frame

    sound.close()

def generate_notes(t=1):
    connect = sqlite3.connect("Audio/frequencies.db")
    cursor = connect.cursor()
    gammes=cursor.execute("SELECT * FROM frequencies")
    notes=["octave","C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    for gamme in gammes :
        for i in range(1,len(gamme)) :
            if (not os.path.isfile("Sounds/"+str(notes[i])+str(gamme[0])+".wav") and t==1) or (not os.path.isfile("Sounds/"+str(notes[i])+str(gamme[0])+"t"+str(t)+"s.wav") and t!=1):
                create_note_wav(gamme[0],notes[i],gamme[i],2*gamme[i],t)


if __name__ == '__main__':
    generate_notes()
