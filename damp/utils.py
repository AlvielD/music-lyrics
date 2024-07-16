import config.genius_config as config
import requests
import re

from lyricsgenius import Genius

# Initialize the Genius API client
genius = Genius(config.ACCESS_TOKEN)

def search_song(song_title, song_artist):
    """Search for a song on Genius and return the first result

    Args:
        song_title (str): title of the song to be searched

    Returns:
        dict: information about the first result of the search
    """
    search_url = f'{config.BASE_URL}/search'
    params = {'q': song_title + ' ' + song_artist}
    response = requests.get(search_url, headers=config.HEADERS, params=params)
    data = response.json()

    if data['response']['hits']:
        return data['response']['hits'][0]['result']
    else:
        return None
    

def get_song_metadata(song_id):
    """Get song's metadata by its Genius ID

    Args:
        song_id (str): ID of the song

    Returns:
        dict: metadata of the requested song
    """
    song_url = f'{config.BASE_URL}/songs/{song_id}'
    response = requests.get(song_url, headers=config.HEADERS)
    return response.json()


def get_song_langugage(song_title, song_artist):
    song = search_song(song_title, song_artist)
    song_id = song['id']

    metadata = get_song_metadata(song_id)['response']
    return metadata['song']['language']


# Function to clean the lyrics from lyricsgenius
def clean_lyrics(lyrics):
    # Check for "You might also like" followed by a '[' without a newline
    lyrics_cleaned = re.sub(r'You might also like(?=\[)', '\n', lyrics)

    # Ensure there is a newline before any '['
    lyrics_cleaned = re.sub(r'(?<!\n)\[', '\n[', lyrics_cleaned)

    # Reduce consecutive newlines to a single newline
    lyrics_cleaned = re.sub(r'\n+', '\n', lyrics_cleaned)

    return lyrics_cleaned.strip()


def scrape_song_lyrics(song_title, artist_name):
    # Search for the song by title and artist
    song = genius.search_song(song_title, artist_name)
    
    if song:
        # Clean lyrics to remove "You might also like" issue
        cleaned_lyrics = clean_lyrics(song.lyrics)

        # Prepare the song data
        song_data = {
            'title': song.title,
            'artist': song.artist,
            'lyrics': cleaned_lyrics
            #song_writers TODO
        }
        
        print(f"Lyrics scraped succesfully")
        return song_data
    else:
        print(f"Lyrics for '{song_title}' by {artist_name} not found.")
        return False