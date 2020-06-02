# https://fr.wikipedia.org/wiki/Note_de_musique
import sqlite3

def octave_min_max(min,max):
    connect = sqlite3.connect("Audio/frequencies.db")
    cursor = connect.cursor()
    cursor.execute("DROP TABLE IF EXISTS frequencies")
    cursor.execute("CREATE TABLE frequencies ( \
                    octave INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
                    C float,\
                    CSharp float,\
                    D  float,\
                    DSharp float,\
                    E float,\
                    F float,\
                    FSharp float,\
                    G float,\
                    GSharp float,\
                    A      float,\
                    ASharp float,\
                    B float\
                    );")
    f0=27.5*2**min
    frequencies=[]
    for i in range(min,max+1):
       octave=[]
       octave.append(i)
       for j in range (-9,3) :
            frequency=f0*2**(j/12.0)
            octave.append(frequency)
       f0*=2
       frequencies.append(octave)
    cursor.executemany("INSERT INTO frequencies VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);", frequencies)
    connect.commit()
    print("yo")
