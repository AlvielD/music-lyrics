from collections import defaultdict
import os
import regex as re
import DALI as dali_code


def display_languages(dali_data):
    # Initialize a dictionary to store language counts and IDs
    language_data = defaultdict(lambda: {'count': 0, 'ids': []})

    # Iterate through all files in dali_data
    for key, entry in dali_data.items():
        # Extract the language and ID from each entry
        language = entry.info['metadata']['language']
        file_id = entry.info['id']
        
        # Update the language data
        language_data[language]['count'] += 1
        language_data[language]['ids'].append(file_id)

    # Display the results
    for language, data in language_data.items():
        print(f"Language: {language}")
        print(f"Count: {data['count']}")
        print(f"IDs: {', '.join(data['ids'])}")
        print("------")


def get_all_artists(dali_data):
    artists = set()  # Using a set to avoid duplicate artists

    # Loop through all files in the dataset directory
    for key, entry in dali_data.items():
        # Extract the artist name
        artist = entry.info['artist']
        if artist:
            artists.add(artist)

    # Convert set to list and sort it
    sorted_artists = sorted(artists)
    return sorted_artists

def get_specific_song(dali_data, title, artist):
    for key, entry in dali_data.items():
        # Extract the artist name
        if entry.info['title']==title and entry.info['artist']==artist:
            return entry.info['id']
    return 'The song is not present in DALI dataset.'   

def get_songs_from_artist(dali_data, artist):
    songs_id = []
    for key, entry in dali_data.items():
        # Extract the artist name
        if entry.info['artist']==artist:
            songs_id.append(entry.info['id'])
    return songs_id  


#Loop to create all DALI json files
def loop_extract_json(DALI_gz_dir, save_path):
    dali_data = dali_code.get_the_DALI_dataset(DALI_gz_dir, skip=[], keep=[])
    
    for item in os.listdir(DALI_gz_dir):
        try:
            entry = dali_data[item.split('.')[0]]
            if not(item == 'info' or item =='__MACOSX'):
                if not(entry.info['metadata']['language']=='polish' or entry.info['metadata']['language']=='croatian' or entry.info['metadata']['language']=='estonian' or entry.info['metadata']['language']=='latin'):
                    name = f"my_annot_name_{item.split('.')[0]}"
                    entry.write_json(save_path, name)
        except:
            pass


def save_to_json(dali_data, path_save, id) :
    entry = dali_data[id]
    name = f"my_annot_name_{id}"
    entry.write_json(path_save, name)