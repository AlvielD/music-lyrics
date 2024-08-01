import json
import os
import utils
import time

from GeniusCompiler import GeniusCompiler
from SpotiScraper import SpotiScraper
from LyricsAnnot import LyricsAnnot

from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm


# Define Asian languages and their corresponding scripts
asian_languages = {
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean',
    'th': 'Thai',
    'vi': 'Vietnamese',
}

def process_damp_metadata_file(metadata_file, dir, DAMP_dir, save_path, id_file_path):
    try:
        # Get track metadata from the metadata file
        track_metadata = utils.read_arrangement_file(f"{DAMP_dir}{dir}/{dir}ArrangementMeta/{metadata_file}")

        title = utils.parse_title(track_metadata['Arrangement title'])
        artists = utils.parse_artist_names(track_metadata['Arrangement artist'])

        file_path = f"{DAMP_dir}{dir}/{dir}Lyrics/{metadata_file.split('.')[0]}.json"

        # Read JSON file
        with open(file_path, encoding='utf-8') as file:
            data = json.load(file)

        # Clean the lyrics
        data = utils.clean_damp_json(data)
        if utils.compute_avg_line_len(data) > 7.0:
            # Create annotations
            annot = LyricsAnnot(title, artists[0])
            annot.build_annotations(data, 'DAMP')
            success = annot.add_section_info()
            
            if success:
                annot.save_to_json(save_path, id_file_path)
        
        return f"Success: {metadata_file}"
    except Exception as ex:
        return f"Error processing {metadata_file}: {ex}"

    
def process_dali_file(metadata_file, DALI_dir, save_path, avoided_songs_file_path, id_file_path):
    try:
        # Get track metadata
        file_path = f"{DALI_dir}{metadata_file.split('.')[0]}.json"

        # Load the existing dictionary from the file
        if os.path.exists(avoided_songs_file_path):
            with open(avoided_songs_file_path, 'r') as avoided_file:
                try:
                    avoided_songs = json.load(avoided_file)
                except json.JSONDecodeError:
                    avoided_songs = {}
        else:
            avoided_songs = {}

        with open(file_path, encoding='utf-8') as file:
            data = json.load(file)
            title = data['info']['title']
            artists = utils.parse_artist_names(data['info']['artist'])

        # Clean the lyrics
        entry = data['annotations']['annot']['lines']
        entry = utils.clean_dali_json(entry)
        
        # Create annotations
        annot = LyricsAnnot(title, artists[0])
        if not(annot.language in asian_languages or annot.language==None):
            annot.build_annotations(data, 'DALI')
            success = annot.add_section_info()
            
            if success:
                annot.save_to_json(save_path, id_file_path)
            return f"Success: {metadata_file}"
        else :
            new_avoided_song_key = f"{title} - {artists[0]}"
            new_avoided_song = {new_avoided_song_key : data['info']['id']}
            if new_avoided_song_key not in avoided_songs:
                # Append the new entry
                avoided_songs.update(new_avoided_song)

                # Save the updated dictionary back to the file
                with open(avoided_songs_file_path, 'w') as avoided_file:
                    json.dump(avoided_songs, avoided_file, indent=4)

    except Exception as ex:
        return f"Error processing {metadata_file}: {ex}"
    
# Check if the text file containing the id of already converted songs is up-to-date compared
# to the actual content of the output folder
# Note: this is a very simple check so as to lower performance needs (number of id must match number of files)
def check_id_list(save_path, id_file_path):
    try:
        # Count the number of files in the save_path directory
        file_count = len([f for f in os.listdir(save_path) if os.path.isfile(os.path.join(save_path, f))])

        # Load the dictionary from the JSON file
        if os.path.exists(id_file_path):
            with open(id_file_path, 'r') as id_file:
                try:
                    id_list = json.load(id_file)
                except json.JSONDecodeError:
                    raise ValueError("The id file contains invalid JSON.")
        else:
            raise FileNotFoundError("The id file does not exist.")

        # Count the number of items in the id_list
        id_count = len(id_list)

        # Check if the file count matches the id count
        if file_count == id_count:
            return True
        else:
            return False

    except Exception as ex:
        return f"Error checking ID list: {ex}"


def update_id_list(save_path, id_file_path):
    try:
        # Initialize an empty dictionary
        id_list = {}

        # Iterate through each file in the save_path directory
        for filename in os.listdir(save_path):
            if filename.endswith('.json'):
                file_path = os.path.join(save_path, filename)
                
                # Load the JSON file content
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    
                    # Extract the title, artist, and song_id
                    title = data['meta']['title']
                    artist = data['meta']['artist']
                    song_id = filename.split('.')[0]  # Remove the '.json' extension to get the ID

                    # Create the key as "title - artist"
                    new_id_key = f"{title} - {artist}"
                    
                    # Add to the dictionary
                    id_list[new_id_key] = song_id

        # Write the dictionary to the id_file_path, overwriting existing content
        with open(id_file_path, 'w', encoding='utf-8') as id_file:
            json.dump(id_list, id_file, indent=4)

        return "ID list updated successfully."

    except Exception as ex:
        return f"Error updating ID list: {ex}"
    

def create_damp_notations(DAMP_dir, save_path, id_file_path, batch_size=10, pause_interval=30, pause_duration=60):
    if not(check_id_list(save_path, id_file_path)):
        update_id_list(save_path, id_file_path)
    lan_dirs = os.listdir(DAMP_dir)
    for dir in lan_dirs:
        print(f"Creating notations for {dir} language")
        metadata_files = os.listdir(f"{DAMP_dir}{dir}/{dir}ArrangementMeta/")
        
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            futures = []
            processed_count = 0
            
            for metadata_file in metadata_files:
                futures.append(executor.submit(process_damp_metadata_file, metadata_file, dir, DAMP_dir, save_path, id_file_path))
                processed_count += 1

                # If the number of processed futures is a multiple of the pause interval, pause the execution
                if processed_count % pause_interval == 0:
                    print(f"Processed {processed_count} files, pausing for {pause_duration} seconds...")
                    time.sleep(pause_duration)
            
            for future in tqdm(as_completed(futures), total=len(metadata_files)):
                result = future.result()
                print(result)
    
def create_dali_notations(DALI_dir, save_path, avoided_songs_file_path, id_file_path, batch_size=10, pause_interval=30, pause_duration=60):
    if not(check_id_list(save_path, id_file_path)):
        update_id_list(save_path, id_file_path)
    lan_files = os.listdir(DALI_dir)
    for file in lan_files:
        print(f"Creating notations for the file {file}")
        
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            futures = []
            processed_count = 0
            
            futures.append(executor.submit(process_dali_file, file, DALI_dir, save_path, avoided_songs_file_path, id_file_path))
            processed_count += 1

            # If the number of processed futures is a multiple of the pause interval, pause the execution
            if processed_count % pause_interval == 0:
                print(f"Processed {processed_count} files, pausing for {pause_duration} seconds...")
                time.sleep(pause_duration)
            
            for future in tqdm(as_completed(futures), total=len(lan_files)):
                result = future.result()
                print(result)
        


def main():
    #TODO: to be updated with the latest versions of the functions above


    DAMP_dir = "./data/toy_DAMP/"
    #DAMP_dir = "./data/DAMP_MVP/sing_300x30x2/"
    DALI_dir = "./dali/dali_json/"
    save_path = "./conversion/saved"
    avoided_songs_file_path = "./conversion/avoided_songs.txt"

    # DAMP NOTATIONS
    lan_dirs = os.listdir(DAMP_dir)
    for dir in lan_dirs:
        print(f"Creating notations for {dir} language")
        metadata_files = os.listdir(f"{DAMP_dir}{dir}/{dir}ArrangementMeta/")
        for i, metadata_file in zip(tqdm(range(len(metadata_files))), metadata_files):
            try:
                # Get track metadata
                file_path = f"{DALI_dir}{metadata_file.split('.')[0]}.json"

                with open(file_path, encoding='utf-8') as file:
                    data = json.load(file)
                    title = data['info']['title']
                    artists = utils.parse_artist_names(data['info']['artist'])

                # Clean the lyrics
                entry = data['annotations']['annot']['lines']
                entry = utils.clean_dali_json(entry)

                annot = LyricsAnnot(title, artists[0])
                annot.build_annotations(data, 'DAMP')
                success = annot.add_section_info()
                
                if success:
                    annot.save_to_json(save_path)
            except Exception as ex:
                print(ex)
    
    # DALI NOTATIONS
    lan_dirs = os.listdir(DALI_dir)
    # Load the existing dictionary from the file
    if os.path.exists(avoided_songs_file_path):
        with open(avoided_songs_file_path, 'r') as avoided_file:
            try:
                avoided_songs = json.load(avoided_file)
                print('1')
            except json.JSONDecodeError:
                avoided_songs = {}
    else:
        avoided_songs = {}
    for file in lan_dirs:
        print(f"Creating notations for the file {file}")
        for i, file in zip(tqdm(range(len(lan_dirs))), lan_dirs):
            try:
                # Get track metadata
                file_path = f"{DAMP_dir}{dir}/{dir}Lyrics/{metadata_file.split('.')[0]}.json"

                # Read JSON file
                with open(file_path, encoding='utf-8') as file:
                    data = json.load(file)

                # Clean the lyrics
                data = utils.clean_dali_json(data)
                
                # Create annotations
                annot = LyricsAnnot(title, artists[0])
                if not(annot.language in asian_languages or annot.language==None):
                    annot.build_annotations(data, 'DALI')
                    success = annot.add_section_info()
            
                    if success:
                        annot.save_to_json(save_path)
                    return f"Success: {metadata_file}"
                else :
                    new_avoided_song_key = f"{title} - {artists[0]}"
                    new_avoided_song = {new_avoided_song_key : data['info']['id']}
                    if new_avoided_song_key not in avoided_songs:
                        # Append the new entry
                        avoided_songs.update(new_avoided_song)

                        # Save the updated dictionary back to the file
                        with open(avoided_songs_file_path, 'w') as avoided_file:
                            json.dump(avoided_songs, avoided_file, indent=4)
            except Exception as ex:
                print(ex)
            

if __name__ == '__main__':
    #main()
    #DAMP_dir = "./data/DAMP_MVP/sing_300x30x2/"
    DALI_dir = "../dali/dali_json/"
    save_path = "./saved/"
    metadata_file = "my_annot_name_022411a432334ca2800c07dfc81848a2.json"
    process_dali_file(metadata_file, DALI_dir, save_path)
    #create_dali_notations(DALI_dir, save_path)