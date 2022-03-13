# Insertion des notes sur la tablature

from PIL import Image, ImageFont, ImageDraw
import random

def generate_tab_for_parameters(fondamentale,gamme,notesMax):
    img = Image.open("../../assets/tab.png")

    font = ImageFont.truetype(font='Arial.ttf', size=18)

    # Definition des dimensions
    note1 = 50
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

    dim_notes = [note1, note2, note3, note4, note5, note6, note7, note8, note9, note10, note11, note12, note13, note14,
                 note15, note16]

    cordeE = 95
    cordeA = 80
    cordeD = 66
    cordeG = 52
    cordeB = 38
    cordeE2 = 24

    d1 = ImageDraw.Draw(img)

    for i in range(notesMax):
        k = random.choice(gamme)
        if (k == 0):
            d1.text((dim_notes[i], cordeE), str(fondamentale), fill=(0, 0, 0), font=font)
        elif (k == 1):
            d1.text((dim_notes[i], cordeE), str(fondamentale + 1), fill=(0, 0, 0), font=font)
        elif (k == 2):
            d1.text((dim_notes[i], cordeE), str(fondamentale + 2), fill=(0, 0, 0), font=font)
        elif (k == 3):
            d1.text((dim_notes[i], cordeE), str(fondamentale + 3), fill=(0, 0, 0), font=font)
        elif (k == 4):
            d1.text((dim_notes[i], cordeA), str(fondamentale - 1), fill=(0, 0, 0), font=font)
        elif (k == 5):
            d1.text((dim_notes[i], cordeA), str(fondamentale), fill=(0, 0, 0), font=font)
        elif (k == 6):
            d1.text((dim_notes[i], cordeA), str(fondamentale + 1), fill=(0, 0, 0), font=font)
        elif (k == 7):
            d1.text((dim_notes[i], cordeA), str(fondamentale + 2), fill=(0, 0, 0), font=font)
        elif (k == 8):
            d1.text((dim_notes[i], cordeA), str(fondamentale + 3), fill=(0, 0, 0), font=font)
        elif (k == 9):
            d1.text((dim_notes[i], cordeD), str(fondamentale - 1), fill=(0, 0, 0), font=font)
        elif (k == 10):
            d1.text((dim_notes[i], cordeD), str(fondamentale), fill=(0, 0, 0), font=font)
        else :
            d1.text((dim_notes[i], cordeD), str(fondamentale + 1), fill=(0, 0, 0), font=font)

    # img.show()
    img.save("../../assets/img_bin/generated_tab.jpg")

    return None