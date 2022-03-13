# Imports
import random
import requests
from bs4 import BeautifulSoup
import os
import re
from fpdf import FPDF
from PIL import Image, ImageFont, ImageDraw

# Parameters

ARTIST = 'Haken'
NB_OF_SONG_FROM_ARTIST = 5
NB_OF_LYRICS_VERSE = 8
NB_OF_LYRICS_CHORUS = 4

# Import api token
GENIUS_API_TOKEN='ABSJKXJDJZGjXN3HJ2BvHaQnoWa71aKojhCsNX-T9mI39EySw6JjCArBXAYx-xvW'

# Fixed parameters

all_root_notes = ['E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#']
all_scales = ["Majeur", "Mineur", "Lydien", "Aeolien", "Mixolydien", "Dorian"]
all_time_signatures = ["4/4", "6/8", "7/8", "9/8"]

chosen_root_note = all_root_notes[3]
chosen_scale = all_scales[0]
chosen_time_signature = all_time_signatures[0]

# fonctions

def turn_chords_tab_to_str(chords_tab):
    chords_list = ''
    for i in range(len(chords_tab)):
        chords_list += (str(chords_tab[i]) + '    ')
    return chords_list

def skip_line_in_pdf(size):
    pdf.cell(200, size, txt="", ln=2, align='C')
    return None


# Get artist object from Genius API
def request_artist_info(artist_name, page):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}
    search_url = base_url + '/search?per_page=10&page=' + str(page)
    data = {'q': artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    return response


# Get Genius.com song url's from artist object
def request_song_url(artist_name, song_cap):
    page = 1
    songs = []

    while True:
        response = request_artist_info(artist_name, page)
        json = response.json()
        # Collect up to song_cap song objects from artist
        song_info = []
        for hit in json['response']['hits']:
            if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
                song_info.append(hit)

        # Collect song URL's from song objects
        for song in song_info:
            if (len(songs) < song_cap):
                url = song['result']['url']
                songs.append(url)

        if (len(songs) == song_cap):
            break
        else:
            page += 1

    #print('Found {} songs by {}'.format(len(songs), artist_name))
    return songs

# Scrape lyrics from a Genius.com song URL
def scrape_song_lyrics(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyric_tag = html.find("div", class_="lyrics")
    if lyric_tag is None:
        class_matcher = re.compile("^Lyrics__Container")
        lyric_tags = html.find_all("div", class_=class_matcher)
        if not lyric_tags:
            print(u'Genius page {0} has no lyric tags', url)
            return None
        lyrics = u'\n\n'.join(tag.get_text(separator="\n").strip() for tag in lyric_tags)
    else:
        lyrics = lyric_tag.get_text(separator="\n").strip()

    lyrics.split('<br>')

    #remove identifiers like chorus, verse, etc
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
    #remove empty lines
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
    return lyrics.split("\n")

def generate_song_from_artist(artist, nb_of_songs):
    url = request_song_url(artist, nb_of_songs)
    random_song = url[random.randint(0, nb_of_songs - 1)]
    return random_song

def generate_lyrics_from_song(song_url):
    all_lyrics = scrape_song_lyrics(song_url)
    return all_lyrics[random.randint(0, len(all_lyrics)) - 1]

def generate_n_lyrics_from_song(artist, nb_of_songs, nb_of_lyrics_to_generate):
    chosen_song = generate_song_from_artist(artist, nb_of_songs)
    print(chosen_song)
    tab_of_generated_lyrics = []
    for k in range(nb_of_lyrics_to_generate):
        tab_of_generated_lyrics.append(generate_lyrics_from_song(chosen_song))
    return tab_of_generated_lyrics

def generate_n_lyrics_from_artist(artist, nb_of_songs, nb_of_lyrics_to_generate):
    tab_of_generated_lyrics = []
    for k in range(nb_of_lyrics_to_generate):
        chosen_song = generate_song_from_artist(artist, nb_of_songs)
        tab_of_generated_lyrics.append(generate_lyrics_from_song(chosen_song))
    return tab_of_generated_lyrics


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


generated_root_note, generated_scale, generated_time_signature = generate_melody(
    chosen_root_note, chosen_scale, chosen_time_signature)

# Then generate melody with generated scale

generate_tab_for_parameters(generated_root_note, generated_scale, generated_time_signature)

# The image is saved in '../../assets/img_bin/generated_tab.jpg'

# Generate chords

chords_1 = generate_chords(generated_root_note, generated_scale)
chords_2 = generate_chords(generated_root_note, generated_scale)

# Generate lyrics

# SKIP

lyrics_verse_1 = generate_n_lyrics_from_artist(ARTIST, NB_OF_SONG_FROM_ARTIST, NB_OF_LYRICS_VERSE)
lyrics_verse_2 = generate_n_lyrics_from_artist(ARTIST, NB_OF_SONG_FROM_ARTIST, NB_OF_LYRICS_VERSE)
lyrics_chorus = generate_n_lyrics_from_artist(ARTIST, NB_OF_SONG_FROM_ARTIST, NB_OF_LYRICS_CHORUS)

# TEMP

# lyrics_verse_1 = ['this is a template', 'to be felled', 'with real lyrics ', 'quand j aurai internet mdr']
# lyrics_verse_2 = ['ftgubhkj', 'second template to try', 'nfsnse', 'fsfsfsff dsfdf  dsfds']
# lyrics_chorus = ['Main_generate_lyrics', 'generate_n_lyrics_from_artist']

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