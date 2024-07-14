import config
import spotipy
from spotipy import SpotifyClientCredentials

class SpotiScraper():
    def __init__(self):
        # Inicializar el cliente de Spotify
        self.sp_client = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=config.CLIENT_TOKEN,
            client_secret=config.CLIENT_SECRET_TOKEN))
    

    def search_song_on_spotify(self, song_title, artist_name):
        query = f"track:{song_title} artist:{artist_name}"
        result = self.sp_client.search(q=query, type='track', limit=1)
        return result


    def get_song_duration(self, song_title, song_artist):
        # Buscar la canción en Spotify
        spotify_response = self.search_song_on_spotify(song_title, song_artist)
        if not spotify_response['tracks']['items']:
            print(f"No se encontró la canción {song_title} de {song_artist} en Spotify.")
            return None

        # Obtener la duración de la canción
        track_info = spotify_response['tracks']['items'][0]
        duration_ms = track_info['duration_ms']
        duration_sec = duration_ms / 1000

        return duration_sec