import json
import os

# Get the ID of a specific song
def get_song_id_by_artist_title(artist, title, id_file_path):
    with open(id_file_path, 'r', encoding='utf-8') as file:
        id_list = json.load(file)

        # Create the key as "title - artist"
        id_key = f"{title} - {artist}"
        
        if id_list[id_key]:
            return id_list[id_key][0]
        else :
            return "This song is not part of our dataset."


# Get the IDs of all the songs by a specific artist
def get_all_song_ids_by_artist(artist, id_file_path):
    song_ids = []
    with open(id_file_path, 'r', encoding='utf-8') as file:
        id_list = json.load(file)
    song_ids = []
    for key, value in id_list.items():
        # Split the key by " - " and check if the second part matches the artist
        key_parts = key.split(" - ")
        if len(key_parts) > 1 and key_parts[1].strip().lower() == artist.lower():
            song_ids.append(value[0])
    
    return song_ids

# Get the IDs of all the songs by a specific artist
def get_all_songs_by_artist(artist, id_file_path):
    song_ids = []
    with open(id_file_path, 'r', encoding='utf-8') as file:
        id_list = json.load(file)
    song_ids = []
    for key, value in id_list.items():
        # Split the key by " - " and check if the second part matches the artist
        key_parts = key.split(" - ")
        if len(key_parts) > 1 and key_parts[1].strip().lower() == artist.lower():
            song_ids.append(key_parts[0])
    
    return song_ids


# Print the content of a song's file
def print_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        print(content)


# Get the 
def get_song_ids_with_single_paragraph(directory='songs'):
    song_ids = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                data = json.load(file)
                if len(data['annotations']) == 1:
                    song_ids.append(data['meta']['song_id'])
    return song_ids