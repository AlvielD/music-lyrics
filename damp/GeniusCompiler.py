import config.genius_config as config
import re

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
    

    def get_lyrics(self, song_title, song_artist):
        # Search for the song on Genius
        song = self.genius.search_song(song_title, song_artist)

        if song:
            # Clean lyrics to remove "You might also like" issue
            lyrics = self.__clean_lyrics(song.lyrics)

            # Prepare the song data
            song_data = {
                'title': song.title,
                'artist': song.artist,
                'lyrics': lyrics
                #song_writers TODO
            }
            
            print(f"Lyrics scraped succesfully")
        else:
            print(f"Lyrics for '{song_title}' by {song_artist} not found.")
            song_data = False

        return song_data
    

    def split_by_section(self, genius_data):

        # Split the lyrics based on the headers
        genius_paragraphs = {}
        lines = genius_data['lyrics'].splitlines()

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
                    singer_names = [genius_data['artist']]  # Default to original artist if no singer specified
                
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
        if genius_paragraphs:
            for name, content_info in genius_paragraphs.items():
                print(f"Paragraph Name: {name}")
                print(f"Content: {content_info['content']}")
                print(f"Singer(s): {', '.join(content_info['singer'])}")
                print("------")
        else:
            print("The provided lyrics does not contain information about sections")
            genius_paragraphs = False

        return genius_paragraphs