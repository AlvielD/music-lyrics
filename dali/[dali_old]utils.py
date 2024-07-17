import requests
import DALI as dali_code
from lyricsgenius import Genius
import re # Search and manipulate strings
import config
import os
import json

# GLOBAL VARIABLES FOR DIRECTORIES
# Path of the dali_data 
DALI_DATA_PATH = r'D:\0_Maud\Etudes\4_ECL\G2\S8\Cours Bologne\Knowledge Engineering\Project\ke_final_project-july24\dali\DALI_v1.0'
# Path of where to save the json of the dali file
DALI_SAVE_JSON_FILE_PATH = r'D:\0_Maud\Etudes\4_ECL\G2\S8\Cours Bologne\Knowledge Engineering\Project\ke_final_project-july24\dali\dali_json'
# Path of where to save the json of the Genius file (before parsing)
GENIUS_SAVE_JSON_FILE_PATH = r'D:\0_Maud\Etudes\4_ECL\G2\S8\Cours Bologne\Knowledge Engineering\Project\ke_final_project-july24\dali\json_lyrics_genius'
# Path of where to save the json of the Genius file with the parsed lyrics
GENIUS_SAVE_PARSED_JSON_FILE_PATH = r'D:\0_Maud\Etudes\4_ECL\G2\S8\Cours Bologne\Knowledge Engineering\Project\ke_final_project-july24\dali\json_parsed_lyrics_genius'
# Path of where to save the final json file
FINAL_OUTPUT_PATH = r'D:\0_Maud\Etudes\4_ECL\G2\S8\Cours Bologne\Knowledge Engineering\Project\ke_final_project-july24\dali\final_json'


# Initialize the Genius API client
genius = Genius(config.ACCESS_TOKEN)


# Function to clean the lyrics from lyricsgenius
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
            #song_writers TODO
        }

        # Save the lyrics to a JSON file
        with open(file_path, 'w') as file:
            json.dump(song_data, file, indent=4)
        
        print(f"Lyrics saved to {file_path}")
    else:
        print(f"Lyrics for '{song_title}' by {artist_name} not found.")


# Function to export a json of the lyrics parsed into paragraphs with headers
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
                paragraph_name = f"{paragraph_name} {header_count[paragraph_name]}"
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




# Function to export a specific song to JSON
def export_dali_json(dali_song_id):
    dali_data = dali_code.get_the_DALI_dataset(DALI_DATA_PATH, skip=[], keep=[])
    entry = dali_data[dali_song_id]

    name = 'my_annot_name_' + dali_song_id

    entry.write_json(DALI_SAVE_JSON_FILE_PATH, name)
    print(f"Exported {name} to {DALI_SAVE_JSON_FILE_PATH}")


# Function to enrich a specific dali file with Genius info and then convert it to JSON
def convert_dali_genius_json(dali_song_id):
    dali_data = dali_code.get_the_DALI_dataset(DALI_DATA_PATH, skip=[], keep=[])
    
    # Create the JSON file of the dali song and export it
    export_dali_json(dali_song_id)

    # Import it to be able to manipulate it
    dali_data = dali_code.Annotations().read_json(os.path.join(DALI_SAVE_JSON_FILE_PATH, 'my_annot_name_'+dali_song_id+'.json'))

    dali_song_data = dali_data[dali_song_id]
    artist_name = dali_song_data.info['artist']
    song_title = dali_song_data.info['title']


    # Create the JSON file of the related song on Genius
    save_song_lyrics_as_json(artist_name, song_title, GENIUS_SAVE_JSON_FILE_PATH)

    # Load it to be able to manipulate it
    file_name = f"{artist_name}_{song_title}.json".replace(' ', '_')
    file_path = os.path.join(GENIUS_SAVE_JSON_FILE_PATH, file_name)
    with open(file_path, 'r') as file:
        genius_data = json.load(file)


    # Create the JSON file of the parsed lyrics from Genius 
    parse_genius_lyrics(file_path, GENIUS_SAVE_PARSED_JSON_FILE_PATH)

    # Load it to be able to manipulate it
    file_name = f"{os.path.splitext(os.path.basename(file_path))[0]}_parsed.json"
    file_path = os.path.join(GENIUS_SAVE_PARSED_JSON_FILE_PATH, file_name)
    with open(file_path, 'r') as file:
        genius_parsed_data = json.load(file)

    # Initialize a list to store the merged annotations
    merged_annotations = []
    
    # Initialize variables to track current paragraph and its content
    current_paragraph_name = None
    current_paragraph_content = None
    current_paragraph_start_time = None
    current_paragraph_end_time = None
    
    # Iterate through DALI lines and match with Genius paragraphs
    for line in dali_song_data.annotations['annot']['lines']:
        line_text = line['text']
        line_start_time = line['time'][0]
        line_end_time = line['time'][1]
        
        # Check if current line belongs to the current paragraph
        if current_paragraph_content and line_text in current_paragraph_content:
            # Add line information to current paragraph
            lines = {
                'line': line_text,
                'time_index': [line_start_time, line_end_time],
                'time_duration': line_end_time - line_start_time
            }
            merged_annotations[-1]['lines'].append(lines)
            
            # Update current paragraph end time
            current_paragraph_end_time = line_end_time
        
        else:
            # If current line doesn't belong to current paragraph, finalize current paragraph
            if current_paragraph_name:
                merged_annotations[-1]['time_index'] = [current_paragraph_start_time, current_paragraph_end_time]
            
            # Move to a new paragraph section
            for paragraph_name, paragraph_info in genius_parsed_data.items():
                paragraph_content = paragraph_info['content']
                singer = paragraph_info['singer']
                
                # Check if current line starts a new paragraph
                if paragraph_content.startswith(line_text):
                    # Initialize new paragraph
                    current_paragraph_name = paragraph_name
                    current_paragraph_content = paragraph_content
                    current_paragraph_start_time = line_start_time
                    current_paragraph_end_time = line_end_time
                    
                    # Add new annotation for the paragraph
                    annotation_data = {
                        'paragraph': current_paragraph_name,
                        'time_index': [current_paragraph_start_time, current_paragraph_end_time],
                        'time_duration': current_paragraph_end_time - current_paragraph_start_time,
                        'singer': singer,
                        'lines': [{
                            'line': line_text,
                            'time_index': [line_start_time, line_end_time],
                            'time_duration': line_end_time - line_start_time
                        }]
                    }
                    
                    merged_annotations.append(annotation_data)
                    
                    break  # Stop searching for paragraph after finding match

    # Finalize last paragraph if any
    if current_paragraph_name:
        merged_annotations[-1]['time_index'] = [current_paragraph_start_time, current_paragraph_end_time]
    
    # Prepare merged data structure
    merged_data = {
        'meta-data': {
            'song_id': dali_song_data.info['id'], # We keep the DALI ID for now (TODO: run a function to change them all starting from 1)
            'title': dali_song_data.info['title'],  # Adjust accordingly based on your JSON structure
            'singer': dali_song_data.info['artist'],  # Adjust accordingly based on your JSON structure
            'song_writer': 'To retrieve from Spotify API?',  # Placeholder for song writer
            'language': dali_song_data.info['metadata']['language'],  # Adjust accordingly based on your JSON structure
        },
        'annotations': merged_annotations
    }
    
    # TODO: delete the temporary json files as we don't need them anymore?

    # Construct the full file path
    save_name = f"{artist_name}_{song_title}.json".replace(' ', '_')
    save_path = os.path.join(FINAL_OUTPUT_PATH, file_name)

    # Save merged data to JSON file
    with open(save_path, 'w') as file:
        json.dump(merged_data, file, indent=4)

    # Print the merged JSON data
    print(json.dumps(merged_data, indent=4))

    print(f"Merged JSON data saved to {save_path}")



# Function to enrich all the dali files of a folder with Genius info and then convert it to JSON
def convert_folder_dali_genius_json():
    dali_data = dali_code.get_the_DALI_dataset(DALI_DATA_PATH, skip=[], keep=[])
    count=1

    for dali_song_id in dali_data:
        convert_dali_genius_json(dali_song_id)
        print(f"Song n°{count} (id: {dali_song_id}) converted to the JSON final output!")
        count+=1

