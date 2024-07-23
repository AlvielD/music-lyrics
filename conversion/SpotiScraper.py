import spotipy
import pprint
import config.spoti_config as config
from spotipy import SpotifyClientCredentials

class SpotiScraper():
    def __init__(self):
        # Initiate Spotify's client
        self.sp_client = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=config.CLIENT_TOKEN,
            client_secret=config.CLIENT_SECRET_TOKEN))
    

    def search_song_on_spotify(self, song_title, artist_name):
        query = f"{song_title} {artist_name}"
        result = self.sp_client.search(q=query, type='track', limit=1)
        return result


    def get_song_duration(self, song_title, song_artist):
        # Search for the song on Spotify
        spotify_response = self.search_song_on_spotify(song_title, song_artist)
        if not spotify_response['tracks']['items']:
            print(f"We did not find the song {song_title} from {song_artist} on Spotify.")
            return None

        # Obtain the duration of the song
        track_info = spotify_response['tracks']['items'][0]
        duration_ms = track_info['duration_ms']
        duration_sec = duration_ms / 1000

        return duration_sec
    

if __name__ == '__main__':
    
    title = 'Blinding Lights'
    artist = 'The Weeknd'

    scraper = SpotiScraper()
    song = scraper.search_song_on_spotify(title, artist)

    print("SCRAPED SONG FROM SPOTIFY:")
    pprint.pprint(song)

    duration = scraper.get_song_duration(title, artist)
    print(f"THE SONG IS {duration}s LONG.")