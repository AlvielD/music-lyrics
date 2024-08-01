import config.genius_config as config
import re
import requests
import translation

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
            
            #print(f"Lyrics scraped successfully")
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
        
        writer_artists = [artist['name'] for artist in song_data['writer_artists']] if song_data['writer_artists'] else [song_data['primary_artist']['name']]

        metadata = {
            'genius_id': song_id,
            'title': song_data['title'],
            'artist': song_data['primary_artist']['name'],
            'language': song_data['language'],
            'writer_artists': writer_artists
        }
        return metadata



    def split_by_section(self, lyrics, artist, original_language, verbose=False):
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
        current_singers = []
        current_paragraph_content = []
        
        header_count = {}

        # Variables to store the last content of specific sections
        last_chorus_content = ''
        last_pre_chorus_content = ''
        last_post_chorus_content = ''

        i = 0

        while i < len(lines):
            line = lines[i]
            match = self.header_pattern.match(line.strip())
            if match:
                # Extract paragraph name and singer(s) if provided
                header_info = match.group(1).strip()
                if ':' in header_info:
                    header_parts = header_info.split(':')
                    paragraph_name = header_parts[0].strip()
                    singer_names = [name.strip() for name in header_parts[1].replace(',', '&').split('&')]
                else:
                    paragraph_name = header_info
                    singer_names = [artist]  # Default to original artist if no singer specified
                
                # Remove numeric suffix if present
                numeric_suffix_match = re.search(r'\d+$', paragraph_name)
                paragraph_name_base = paragraph_name[:numeric_suffix_match.start()].strip() if numeric_suffix_match else paragraph_name

                # Translate paragraph name's base to English
                result = translation.translate_header(paragraph_name_base, original_language)
                if result == 0 : #header in the original language did not match anything in the translation dictionary
                    print(f"Warning: Paragraph name '{paragraph_name_base}' in language '{original_language}' is not a standard section name.")
                elif result == 1 : #header in a language not supported by the dictionary
                    print(f'{original_language} is not part of the supported languages.')
                else :
                    paragraph_name_base = result.title()
    
                    # Save the previous paragraph if exists
                    if current_paragraph_name and current_paragraph_content and current_singers:
                        # Adjust previous paragraph occurrence information if it's a duplicate
                        if current_paragraph_name in header_count:
                            header_count[current_paragraph_name] += 1
                        else :
                            header_count[current_paragraph_name] = 1

                        genius_paragraphs[(current_paragraph_name, header_count[current_paragraph_name])] = {
                            'content': ' '.join(current_paragraph_content),
                            'singer': current_singers
                        }

                        # Store the last content of specific sections
                        if "Chorus" in current_paragraph_name and header_count['Chorus'] == 1 :
                            last_chorus_content = ' '.join(current_paragraph_content)
                        elif "Pre-Chorus" in current_paragraph_name and header_count['Pre-Chorus'] == 1 :
                            last_pre_chorus_content = ' '.join(current_paragraph_content)
                        elif "Post-Chorus" in current_paragraph_name and header_count['Post-Chorus'] == 1:
                            last_post_chorus_content = ' '.join(current_paragraph_content)

                    # Check the next line to see if it's content or another section header
                    next_line = lines[i + 1] if i + 1 < len(lines) else ''
                    next_match = self.header_pattern.match(next_line.strip())

                    if paragraph_name_base in ["Chorus", "Pre-Chorus", "Post-Chorus"] and (not next_line.strip() or next_match):
                        # Append last content if the next line is empty or another header
                        if paragraph_name_base == "Chorus" and last_chorus_content:
                            current_paragraph_content = []
                            current_paragraph_content.append(last_chorus_content)
                        elif paragraph_name_base == "Pre-Chorus" and last_pre_chorus_content:
                            current_paragraph_content = []
                            current_paragraph_content.append(last_pre_chorus_content)
                        elif paragraph_name_base == "Post-Chorus" and last_post_chorus_content:
                            current_paragraph_content = []
                            current_paragraph_content.append(last_post_chorus_content)
                    else:
                        current_paragraph_content = []

                    current_paragraph_name = paragraph_name_base
                    current_singers = singer_names
                    

            else:
                current_paragraph_content.append(line)
            
            i += 1

        # Save the last paragraph
        if current_paragraph_name and current_paragraph_content and current_singers:
            # Adjust previous paragraph occurrence information if it's a duplicate
            if current_paragraph_name in header_count:
                header_count[current_paragraph_name] += 1
            else :
                header_count[current_paragraph_name] = 1

            genius_paragraphs[(current_paragraph_name, header_count[current_paragraph_name])] = {
                'content': ' '.join(current_paragraph_content),
                'singer': current_singers
            }


        # Print extracted paragraphs to check
        if genius_paragraphs and verbose:
            for name, content_info in genius_paragraphs.items():
                print(f"Paragraph Name: {name[0]}")
                print(f"Paragraph Occurrence: {name[1]}")
                print(f"Content: {content_info['content']}")
                print(f"Singer(s): {', '.join(content_info['singer'])}")
                print("------")
        elif not(genius_paragraphs):
            print("The provided lyrics do not contain information about sections")
            genius_paragraphs = False

        return genius_paragraphs
        

if __name__ == '__main__':
    
    title = 'Ziggy Un Garçon Pas Comme (avec Séparation)'
    artist = 'Celine Dion'

    # Create an instance of our compiler and scrape the lyrics from Genius
    compiler = GeniusCompiler()
    text = compiler.search_song(title, artist)