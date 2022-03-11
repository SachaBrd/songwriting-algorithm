# Generateur de riffs
# Sacha Bourdeau

from tkinter import *
import random as rand

# Programme principal
# diff

root = Tk()
root.title("Generateur_de_riffs")
photo = PhotoImage(file='assets/tab.gif')
widthim,heightim = photo.width(),photo.height()
can = Canvas(root,width = widthim,height = heightim)
can.create_image(widthim/2,heightim/2,image = photo)
can.pack()

# Donner la fondamentale
label = Label(root, text="Fondamentale : ")
label.pack(side=LEFT)
rootNoteVar = StringVar()
rootNoteVar.set("E")
rootNote = OptionMenu(root, rootNoteVar, 'E','F','F#','G','G#','A','A#','B','C','C#','D','D#')
rootNote.pack(side = LEFT)

# Donner la gamme
label = Label(root, text="Gamme : ")
label.pack(side=LEFT)
ScaleVar = StringVar()
ScaleVar.set("Majeur")
Scale = OptionMenu(root, ScaleVar, "Majeur","Mineur",
                      "Lydien","Aeolien","Mixolydien","Dorian","Chromatique")
Scale.pack(side = LEFT)

# Donner la signature rythmique
label = Label(root, text="Signature rythmique : ")
label.pack(side=LEFT)
TimeSigVar = StringVar()
TimeSigVar.set("4/4")
TimeSig = OptionMenu(root, TimeSigVar, "4/4","6/8","7/8","9/8")
TimeSig.pack(side = LEFT)

# Autoriser les decalages
vals = ['AvecP', 'SansP']
etiqs = ['Avec pauses', 'Sans pauses']
varGr = StringVar()
varGr.set(vals[1])
for i in range(2):
    b = Radiobutton(root, variable=varGr, text=etiqs[i], value=vals[i])
    b.pack(side = LEFT)

Button(root,text = 'Quitter',command = root.destroy).pack(side = RIGHT)

def generate(rootNote,Scale,TimeSig):    
    can.create_image(widthim/2,heightim/2,image = photo)
    rootN = rootNoteVar.get()
    fondamentale = 0;
    # Switch case
    if (rootN) == "E":
        fondamentale = 0
    elif (rootN) == "F":
        fondamentale = 1
    elif (rootN) == "F#":
        fondamentale = 2
    elif (rootN) == "G":
        fondamentale = 3
    elif (rootN) == "G#":
        fondamentale = 4
    elif (rootN) == "A":
        fondamentale = 5
    elif (rootN) == "A#":
        fondamentale = 6
    elif (rootN) == "B":
        fondamentale = 7
    elif (rootN) == "C":
        fondamentale = 8
    elif (rootN) == "C#":
        fondamentale = 9
    elif (rootN) == "D":
        fondamentale = 10
    else:
        fondamentale = 11

    Sc = ScaleVar.get()
    gamme = 0;
    # Switch case
    if (Sc) == "Majeur":
        gamme = [0,2,3,5,7,8,10]
    elif (Sc) == "Mineur":
        gamme = [0,2,3,5,7,8,11]
    elif (Sc) == "Lydien":
        gamme = [0,2,4,6,7,9,11]
    elif (Sc) == "Aeolien":
        gamme = [0,1,3,5,7,8,10]
    elif (Sc) == "Mixolydien":
        gamme = [0,2,4,5,7,9,10]
    elif (Sc) == "Dorian":
        gamme = [0,2,3,5,7,9,10]
    # gamme chromatique
    else:
        gamme = range(11)

    aux = []
    for i in range(len(gamme)):
        aux.append(gamme[(i+fondamentale)%len(gamme)])
    gamme=aux
    gamme.sort()

    TSig = TimeSigVar.get()
    if (TSig) == "4/4":
        notesMax = 8
    elif (TSig) == "6/8":
        notesMax = 12
    elif (TSig) == "7/8":
        notesMax = 7
    else:
        notesMax = 9
    

    # Insertion des notes sur la tablature

    # Definition des dimensions
    note1 = 65
    note2 = note1 + 30
    note3 = note1 + 60
    note4 = note1 + 90
    note5 = note1 + 120
    note6 = note1 + 150
    note7 = note1 + 180
    note8 = note1 + 210
    note9 = note1 + 240
    note10 = note1 + 270
    note11 = note1 + 300
    note12 = note1 + 330
    note13 = note1 + 360
    note14 = note1 + 390
    note15 = note1 + 420
    note16 = note1 + 450

    dim_notes = [note1,note2,note3,note4,note5,note6,note7,note8,note9,note10,note11,note12,note13,note14,note15,note16]
    
    cordeE = 103
    cordeA = 89
    cordeD = 75
    cordeG = 61
    cordeB = 46
    cordeE2 = 33
    
    # Programme principal

    if(varGr.get() == 'SansP'):
        for i in range(notesMax):
            k = rand.choice(gamme)
            if(k == 0):
                can.create_text(dim_notes[i], cordeE, text = fondamentale)
            elif(k == 1):
                can.create_text(dim_notes[i], cordeE, text = fondamentale+1)
            elif(k == 2):
                can.create_text(dim_notes[i], cordeE, text = fondamentale+2)
            elif(k == 3):
                can.create_text(dim_notes[i], cordeE, text = fondamentale+3)
            elif(k == 4):
                can.create_text(dim_notes[i], cordeA, text = fondamentale-1)
            elif(k == 5):
                can.create_text(dim_notes[i], cordeA, text = fondamentale)
            elif(k == 6):
                can.create_text(dim_notes[i], cordeA, text = fondamentale+1)
            elif(k == 7):
                can.create_text(dim_notes[i], cordeA, text = fondamentale+2)
            elif(k == 8):
                can.create_text(dim_notes[i], cordeA, text = fondamentale+3)
            elif(k == 9):
                can.create_text(dim_notes[i], cordeD, text = fondamentale-1)
            elif(k == 10):
                can.create_text(dim_notes[i], cordeD, text = fondamentale)
            else:
                can.create_text(dim_notes[i], cordeD, text = fondamentale+1)
    else:
        skip = [0,0,0,0,0,1]
        for i in range(notesMax):
            k = rand.choice(gamme)
            sk = 0
            if(i < notesMax):
                sk = rand.choice(skip)
            if sk == 0:
                if(k == 0):
                    can.create_text(dim_notes[i], cordeE, text = fondamentale)
                elif(k == 1):
                    can.create_text(dim_notes[i], cordeE, text = fondamentale+1)
                elif(k == 2):
                    can.create_text(dim_notes[i], cordeE, text = fondamentale+2)
                elif(k == 3):
                    can.create_text(dim_notes[i], cordeE, text = fondamentale+3)
                elif(k == 4):
                    can.create_text(dim_notes[i], cordeA, text = fondamentale-1)
                elif(k == 5):
                    can.create_text(dim_notes[i], cordeA, text = fondamentale)
                elif(k == 6):
                    can.create_text(dim_notes[i], cordeA, text = fondamentale+1)
                elif(k == 7):
                    can.create_text(dim_notes[i], cordeA, text = fondamentale+2)
                elif(k == 8):
                    can.create_text(dim_notes[i], cordeA, text = fondamentale+3)
                elif(k == 9):
                    can.create_text(dim_notes[i], cordeD, text = fondamentale-1)
                elif(k == 10):
                    can.create_text(dim_notes[i], cordeD, text = fondamentale)
                else:
                    can.create_text(dim_notes[i], cordeD, text = fondamentale+1)
                

Button(root,text = 'Generer',command = lambda:generate(rootNote,Scale,TimeSig)).pack(side = RIGHT)

root.mainloop()