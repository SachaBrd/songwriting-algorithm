import random

from fpdf import FPDF

from src.generate_structure import Generate_structure, Generate_tab_image
from src.generate_lyrics import Main_generate_lyrics

# Parameters

ARTIST = 'First of october'
NB_OF_SONG_FROM_ARTIST = 5
NB_OF_LYRICS_VERSE = 8
NB_OF_LYRICS_CHORUS = 4


# Fixed parameters

all_root_notes = ['E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#']
all_scales = ["Majeur", "Mineur", "Lydien", "Aeolien", "Mixolydien", "Dorian"]
all_time_signatures = ["4/4", "6/8", "7/8", "9/8"]

chosen_root_note = all_root_notes[3]
chosen_scale = all_scales[0]
chosen_time_signature = all_time_signatures[0]

generated_root_note, generated_scale, generated_time_signature = Generate_structure.generate_melody(
    chosen_root_note, chosen_scale, chosen_time_signature)

# Then generate melody with generated scale

Generate_tab_image.generate_tab_for_parameters(generated_root_note, generated_scale, generated_time_signature)

# The image is saved in '../../assets/img_bin/generated_tab.jpg'

# Generate chords

chords_1 = Generate_structure.generate_chords(generated_root_note, generated_scale)
chords_2 = Generate_structure.generate_chords(generated_root_note, generated_scale)

# Generate lyrics

# SKIP

lyrics_verse_1 = Main_generate_lyrics.generate_n_lyrics_from_artist(ARTIST, NB_OF_SONG_FROM_ARTIST, NB_OF_LYRICS_VERSE)
lyrics_verse_2 = Main_generate_lyrics.generate_n_lyrics_from_artist(ARTIST, NB_OF_SONG_FROM_ARTIST, NB_OF_LYRICS_VERSE)
lyrics_chorus = Main_generate_lyrics.generate_n_lyrics_from_artist(ARTIST, NB_OF_SONG_FROM_ARTIST, NB_OF_LYRICS_CHORUS)

# TEMP

# lyrics_verse_1 = ['this is a template', 'to be felled', 'with real lyrics ', 'quand j aurai internet mdr']
# lyrics_verse_2 = ['ftgubhkj', 'second template to try', 'nfsnse', 'fsfsfsff dsfdf  dsfds']
# lyrics_chorus = ['Main_generate_lyrics', 'generate_n_lyrics_from_artist']

# fonction utile lol

def turn_chords_tab_to_str(chords_tab):
    chords_list = ''
    for i in range(len(chords_tab)):
        chords_list += (str(chords_tab[i]) + '    ')
    return chords_list

def skip_line_in_pdf(size):
    pdf.cell(200, size, txt="", ln=2, align='C')
    return None

# save FPDF() class into a variable pdf
pdf = FPDF()

# Add a page
pdf.add_page()

# Song title is a random part of the chorus

song_title = random.choice([l for l in lyrics_chorus])

# Title
pdf.set_font("Times", size=20)
pdf.cell(200, 10, txt=str(song_title), ln=1, align='C')

# Subtitle
pdf.set_font("Times", size=8)
pdf.cell(200, 10, txt="A randomly generated song in the style of " + ARTIST, ln=2, align='C')

# Saut de ligne
skip_line_in_pdf(8)

pdf.cell(200, 5, txt="In key of " + str(chosen_root_note) + ' ' + str(chosen_scale), ln=2, align='L')
pdf.cell(200, 5, txt="BPM : " + str(random.randint(80, 160)), ln=2, align='L')
pdf.cell(200, 5, txt="Time signature : " + str(chosen_time_signature), ln=2, align='L')

skip_line_in_pdf(8)
pdf.cell(200, 5, txt="Main melody :", ln=2, align='L')

# Image
pdf.image('../../assets/img_bin/generated_tab.jpg', w=90, h=30)

def write_verse(verse_title, chords, lyrics):
    pdf.cell(200, 5, txt=verse_title, ln=2, align='L')
    skip_line_in_pdf(3)
    [(pdf.cell(11, 5, txt=str(l), ln=2, align='L'), pdf.cell(11, 5, txt=turn_chords_tab_to_str(chords),
     ln=2, align='L'), skip_line_in_pdf(3))for l in lyrics]
    return None

# 1st verse
write_verse('[VERSE 1]', chords_1, lyrics_verse_1)
skip_line_in_pdf(8)

# 1st chorus
write_verse('[CHORUS 1]', chords_2, lyrics_chorus)
skip_line_in_pdf(8)

# 2nd verse
write_verse('[VERSE 2]', chords_1, lyrics_verse_2)
skip_line_in_pdf(8)

# 2nd chorus
write_verse('[CHORUS 2]', chords_2, lyrics_chorus)
skip_line_in_pdf(8)

# Bridge
pdf.cell(200, 5, txt="[Bridge + Guitar solo]", ln=2, align='L')
pdf.cell(10, 10, txt=turn_chords_tab_to_str(chords_1), ln=2, align='L')
skip_line_in_pdf(8)

# 3rd chorus
pdf.cell(200, 5, txt="[CHORUS 3]", ln=2, align='L')
skip_line_in_pdf(3)
[(pdf.cell(11, 5, txt=str(l), ln=2, align='L'), pdf.cell(11, 5, txt=turn_chords_tab_to_str(chords_2),
 ln=2, align='L'), skip_line_in_pdf(3)) for l in lyrics_chorus]
[(pdf.cell(11, 5, txt=str(l), ln=2, align='L'), pdf.cell(11, 5, txt=turn_chords_tab_to_str(chords_2),
 ln=2, align='L'), skip_line_in_pdf(3)) for l in lyrics_chorus]

# save the pdf with name .pdf
pdf.output("../../assets/PDF_bin/Randomly_generated_song.pdf")