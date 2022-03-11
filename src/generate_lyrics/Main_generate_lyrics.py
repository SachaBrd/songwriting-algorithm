# Main generate lyrics

# Imports
import random
import requests
from bs4 import BeautifulSoup
import os
import re

# Import api token
GENIUS_API_TOKEN='ABSJKXJDJZGjXN3HJ2BvHaQnoWa71aKojhCsNX-T9mI39EySw6JjCArBXAYx-xvW'


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
    return all_lyrics[random.randint(0, len(all_lyrics))]

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

# -------- MAIN --------

print(generate_n_lyrics_from_song('PNL', 5, 8))
print('\n')
print(generate_n_lyrics_from_artist('PNL', 1, 4))
