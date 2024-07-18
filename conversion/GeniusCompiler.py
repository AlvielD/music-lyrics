import config.genius_config as config
import pprint
import re
import requests

from lyricsgenius import Genius

class GeniusCompiler:
    def __init__(self):
        self.genius = Genius(config.ACCESS_TOKEN)
        self.header_pattern = re.compile(r'\[(.*?)\]')


    def __clean_lyrics(self, lyrics):
        lyrics_cleaned = re.sub(r'You might also like(?=\[)', '\n', lyrics) # Remove "You might also like" followed by a '['
        lyrics_cleaned = re.sub(r'(?<!\n)\[', '\n[', lyrics_cleaned)        # Ensure there is a newline before any '['
        lyrics_cleaned = re.sub(r'\n+', '\n', lyrics_cleaned)               # Reduce consecutive newlines to a single newline

        return lyrics_cleaned.strip()
    

    def get_lyrics(self, title, artist):
        """Scraped lyrics from a song using its title and primary artist name

        Args:
            title (str): song's title
            artist (str): artist's name

        Returns:
            dict: cleaned lyrics of the song.
        """
        song = self.genius.search_song(title, artist)

        if song:
            # Clean lyrics to remove "You might also like" issue
            lyrics = self.__clean_lyrics(song.lyrics)
            
            print(f"Lyrics scraped successfully")
        else:
            print(f"Lyrics for '{title}' by {artist} not found.")
            lyrics = False

        return lyrics
    

    def search_song(self, title, artist):
        return self.genius.search_song(title, artist)
        

    def get_song_metadata(self, song_id):
        """Get song's metadata by its Genius ID

        Args:
            song_id (str): ID of the song

        Returns:
            dict: metadata of the requested song
        """
        song_url = f'{config.BASE_URL}/songs/{song_id}'
        data = requests.get(song_url, headers=config.HEADERS).json()
        song_data = data['response']['song']
        
        writer_artists = [artist['name'] for artist in song_data['writer_artists']]

        metadata = {
            'genius_id': song_id,
            'title': song_data['title'],
            'artist': song_data['primary_artist']['name'],
            'language': song_data['language'],
            'writer_artists': writer_artists
        }
        return metadata


    def split_by_section(self, lyrics, artist, verbose = False):
        """Splits the provided lyrics in sections using the information present on it.

        Args:
            lyrics (str): lyrics scraped from Genius
            artist (str): primary artist name (case when the artist is not mentioned on the scraped information)
            verbose (bool, optional): whether to display some information of the process. Defaults to False.

        Returns:
            dict: lyrics splitted by sections
        """

        # Split the lyrics based on the headers
        genius_paragraphs = {}
        lines = lyrics.splitlines()

        current_paragraph_name = None
        current_paragraph_content = []
        
        header_count = {}

        for line in lines:
            match = self.header_pattern.match(line.strip())
            if match:
                # Save the previous paragraph if exists
                if current_paragraph_name and current_paragraph_content:
                    genius_paragraphs[current_paragraph_name] = {
                        'content': ' '.join(current_paragraph_content),
                        'singer': singer_names
                    }
                
                # Extract paragraph name and singer(s) if provided
                header_info = match.group(1).strip()
                if ':' in header_info:
                    header_parts = header_info.split(':')
                    paragraph_name = header_parts[0].strip()
                    singer_names = [name.strip() for name in header_parts[1].split('&')]
                else:
                    paragraph_name = header_info
                    singer_names = [artist]  # Default to original artist if no singer specified
                
                # Adjust paragraph name if it's a duplicate
                if paragraph_name in header_count:
                    header_count[paragraph_name] += 1
                    paragraph_name = f"{paragraph_name} {header_count[paragraph_name]}"
                else:
                    header_count[paragraph_name] = 1
                
                current_paragraph_name = paragraph_name
                current_paragraph_content = []
            else:
                current_paragraph_content.append(line)

        # Print extracted paragraphs to check
        if genius_paragraphs and verbose:
            for name, content_info in genius_paragraphs.items():
                print(f"Paragraph Name: {name}")
                print(f"Content: {content_info['content']}")
                print(f"Singer(s): {', '.join(content_info['singer'])}")
                print("------")
        elif not(genius_paragraphs):
            print("The provided lyrics does not contain information about sections")
            genius_paragraphs = False

        return genius_paragraphs
    

if __name__ == '__main__':
    
    title = 'Blinding Lights'
    artist = 'The Weeknd'

    # Create an instance of our compiler and scrape the lyrics from Genius
    compiler = GeniusCompiler()
    lyrics = compiler.get_lyrics(title, artist)
    paragraphs = compiler.split_by_section(lyrics, artist, verbose=True)

    pprint.pprint(type(lyrics))