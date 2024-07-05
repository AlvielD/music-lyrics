import requests

# Your MusiXmatch API key
api_key = 'e90a5888fa022a808f82c880494e591b'

# Endpoint for fetching track details
track_search_url = 'https://api.musixmatch.com/ws/1.1/track.search'
lyrics_url = 'https://api.musixmatch.com/ws/1.1/track.lyrics.get'
subtitle_url = 'https://api.musixmatch.com/ws/1.1/track.subtitle.get'
track_url = 'https://api.musixmatch.com/ws/1.1/track.get'

def search_track(track_name, artist_name):
    params = {
        'apikey': api_key,
        'q_track': track_name,
        'q_artist': artist_name,
        #'f_lyrics_language': language,
        'page_size': 1,
        's_track_rating': 'desc'
    }
    response = requests.get(track_search_url, params=params)
    return response.json()

def get_lyrics(track_id):
    params = {
        'apikey': api_key,
        'track_id': track_id
    }
    response = requests.get(lyrics_url, params=params)
    return response.json()

def get_subtitle(track_id): #looslike we cannot access the subtitle without a commercial plan...
    params = {
        'apikey': api_key,
        'track_id': track_id,
        'format': 'json'
    }
    response = requests.get(subtitle_url, params=params)
    return response.json()

def get_track_info(track_id):
    params = {
        'apikey': api_key,
        'track_id': track_id
    }
    response = requests.get(track_url, params=params)
    return response.json()