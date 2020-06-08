import sys
sys.path.append('../Sounds')
from wav_audio import *

''' ouverture des fichiers des trois notes, et récupération de leur liste d'échantillons
Remarque : les trois sons doivent bien entendu avoir été créé avec la même fréquence d'échantillonnage... '''

def generate_chords(harmonics):
    data=[]
    dataX=[]
    for noteSTR in harmonics:
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


if __name__=="__main__":
    accords=['C3','F3','G3']
    data = generate_chords(accords)
