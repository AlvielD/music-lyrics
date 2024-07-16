import config.genius_config as config
import requests

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