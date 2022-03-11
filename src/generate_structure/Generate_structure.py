# Generate structure for a song

import random as rand

liste_notes = ['E','F','F#','G','G#','A','A#','B','C','C#','D','D#']

def generate_to_algorithm(rootN,Sc,TSig):

    # Initialise variables

    fondamentale = 0
    gamme = 0
    notesMax = 0

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

    # Switch case
    if (Sc) == "Majeur":
        gamme = [0, 2, 3, 5, 7, 8, 10]
    elif (Sc) == "Mineur":
        gamme = [0, 2, 3, 5, 7, 8, 11]
    elif (Sc) == "Lydien":
        gamme = [0, 2, 4, 6, 7, 9, 11]
    elif (Sc) == "Aeolien":
        gamme = [0, 1, 3, 5, 7, 8, 10]
    elif (Sc) == "Mixolydien":
        gamme = [0, 2, 4, 5, 7, 9, 10]
    elif (Sc) == "Dorian":
        gamme = [0, 2, 3, 5, 7, 9, 10]
    # gamme chromatique
    else:
        gamme = range(11)

    aux = []
    for i in range(len(gamme)):
        aux.append(gamme[(i + fondamentale) % len(gamme)])
    gamme = aux
    gamme.sort()

    if (TSig) == "4/4":
        notesMax = 8
    elif (TSig) == "6/8":
        notesMax = 12
    elif (TSig) == "7/8":
        notesMax = 7
    else:
        notesMax = 9

    return fondamentale, gamme, notesMax

print(generate_to_algorithm('B', 'Majeur', '4/4'))




