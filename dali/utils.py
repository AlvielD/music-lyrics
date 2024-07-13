import requests
from lyricsgenius import Genius
import re # Search and manipulate strings
import config
import os
import json


# Initialize the Genius API client
genius = Genius(config.ACCESS_TOKEN)


def clean_lyrics(lyrics):
    # Check for "You might also like" followed by a '[' without a newline
    lyrics_cleaned = re.sub(r'You might also like(?=\[)', '\n', lyrics)

    # Ensure there is a newline before any '['
    lyrics_cleaned = re.sub(r'(?<!\n)\[', '\n[', lyrics_cleaned)

    # Reduce consecutive newlines to a single newline
    lyrics_cleaned = re.sub(r'\n+', '\n', lyrics_cleaned)

    return lyrics_cleaned.strip()

# Function to search for a specific song and save the lyrics
def save_song_lyrics_as_json(artist_name, song_title, directory, file_name=None):
    # Search for the song by the artist
    song = genius.search_song(song_title, artist_name)
    
    if song:
        # Clean lyrics to remove "You might also like" issue
        cleaned_lyrics = clean_lyrics(song.lyrics)

        # If no file name is provided, create a default file name
        if not file_name:
            file_name = f"{artist_name}_{song_title}.json".replace(' ', '_')

        # Construct the full file path
        file_path = os.path.join(directory, file_name)

        # Prepare the song data
        song_data = {
            'title': song.title,
            'artist': song.artist,
            'lyrics': cleaned_lyrics
        }

        # Save the lyrics to a JSON file
        with open(file_path, 'w') as file:
            json.dump(song_data, file, indent=4)
        
        print(f"Lyrics saved to {file_path}")
    else:
        print(f"Lyrics for '{song_title}' by {artist_name} not found.")


def parse_genius_lyrics(genius_file, directory):

    with open(genius_file, 'r') as file:
        genius_data = json.load(file)

    genius_lyrics = genius_data['lyrics']

    # Regular expression to match paragraph headers (e.g., [Verse 1], [Chorus], [Pre-Chorus: Artist1 & Artist2], etc.)
    header_pattern = re.compile(r'\[(.*?)\]')

    # Split the lyrics based on the headers
    genius_paragraphs_dict = {}
    lines = genius_lyrics.splitlines()
    current_paragraph_name = None
    current_paragraph_content = []
    header_count = {}

    for line in lines:
        match = header_pattern.match(line.strip())
        if match:
            # Save the previous paragraph if exists
            if current_paragraph_name and current_paragraph_content:
                genius_paragraphs_dict[current_paragraph_name] = {
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
                paragraph_name = f"{paragraph_name}{header_count[paragraph_name]}"
            else:
                header_count[paragraph_name] = 1
            
            current_paragraph_name = paragraph_name
            current_paragraph_content = []
        else:
            current_paragraph_content.append(line)

    # Add the last paragraph if exists
    if current_paragraph_name and current_paragraph_content:
        genius_paragraphs_dict[current_paragraph_name] = {
            'content': ' '.join(current_paragraph_content),
            'singer': singer_names
        }

    # Print extracted paragraphs to check
    for name, content_info in genius_paragraphs_dict.items():
        print(f"Paragraph Name: {name}")
        print(f"Content: {content_info['content']}")
        print(f"Singer(s): {', '.join(content_info['singer'])}")
        print("------")

    # Construct the full file path
    file_name = f"{os.path.splitext(os.path.basename(genius_file))[0]}_parsed.json"
    file_path = os.path.join(directory, file_name)

    # Save the parsed paragraphs as JSON
    with open(file_path, 'w') as outfile:
        json.dump(genius_paragraphs_dict, outfile, indent=4)
    
    print(f"Parsed paragraphs saved to {file_path}")