# Generate structure for a song
import random

def fondamentale_transcription(rootN):
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

    return fondamentale

def gamme_transcription(Sc):
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

    return gamme


def generate_melody(rootN,Sc,TSig):

    # Initialise variables
    notesMax = 0

    fondamentale = fondamentale_transcription(rootN)

    gamme = gamme_transcription(Sc)

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

def generate_chords(fondamentale, Sc):
    dict_notes = {'E': 0 , 'F': 1, 'F#': 2, 'G': 3, 'G#': 4, 'A': 5, 'A#': 6, 'B': 7, 'C': 8, 'C#': 9, 'D': 10, 'D#': 11}
    inv_notes = {v: k for k, v in dict_notes.items()}
    chords = []
    for i in range(4):
        chord = random.choice(gamme_transcription(Sc))
        base = fondamentale_transcription(fondamentale)
        current_chord = chord + base
        if current_chord > 11 :
            current_chord -= 11
        current_chord=inv_notes.get(current_chord)
        chords.append(current_chord)
    return chords


