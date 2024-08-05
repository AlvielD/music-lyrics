import json
import os
import utils
import time
import shutil

from LyricsAnnot import LyricsAnnot
from SongNotFoundException import SongNotFoundException

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

def process_damp_metadata_file(metadata_file, dir, DAMP_dir, save_path, already_converted_path, id_file_path, avoided_songs_file_path):
    try:
        # Get track metadata from the metadata file
        track_metadata = utils.read_arrangement_file(f"{DAMP_dir}{dir}/{dir}ArrangementMeta/{metadata_file}")

        title = utils.parse_title(track_metadata['Arrangement title'])
        artists = utils.parse_artist_names(track_metadata['Arrangement artist'])

        meta_file_path = f"{DAMP_dir}{dir}/{dir}ArrangementMeta/{metadata_file.split('.')[0]}.txt"
        lyrics_file_path = f"{DAMP_dir}{dir}/{dir}Lyrics/{metadata_file.split('.')[0]}.json"

        moved_meta_file_path = f"{already_converted_path}{dir}/{dir}ArrangementMeta/"
        moved_lyrics_file_path = f"{already_converted_path}{dir}/{dir}Lyrics/"

        # Load the existing dictionary of avoided songs from the file
        if os.path.exists(avoided_songs_file_path):
            with open(avoided_songs_file_path, 'r') as avoided_file:
                try:
                    avoided_songs = json.load(avoided_file)
                except json.JSONDecodeError:
                    avoided_songs = {}
        else:
            avoided_songs = {}

        # Read JSON file
        with open(lyrics_file_path, encoding='utf-8') as file:
            data = json.load(file)

        # Clean the lyrics
        data = utils.clean_damp_json(data)
        if utils.compute_avg_line_len(data) > 7.0:
            # Create annotations
            try:
                annot = LyricsAnnot(title, artists[0])
                if not(annot.language==None):
                    annot.build_annotations(data, 'DAMP')
                    success = annot.add_section_info()
                    
                    if success: # song has paragraphs on Genius
                        annot.save_to_json(save_path, id_file_path, 'DAMP')
                    
                    else:
                        new_avoided_song_key = f"{title} - {artists[0]}"
                        new_avoided_song = {new_avoided_song_key : [metadata_file.split('.')[0],'no_paragraphs']}
                        if new_avoided_song_key not in avoided_songs:
                            # Append the new entry
                            avoided_songs.update(new_avoided_song)

                            # Save the updated dictionary back to the file
                            with open(avoided_songs_file_path, 'w') as avoided_file:
                                json.dump(avoided_songs, avoided_file, indent=4)

                else:
                    new_avoided_song_key = f"{title} - {artists[0]}"
                    new_avoided_song = {new_avoided_song_key : [metadata_file.split('.')[0],'no_language_information']}
                    if new_avoided_song_key not in avoided_songs:
                        # Append the new entry
                        avoided_songs.update(new_avoided_song)

                        # Save the updated dictionary back to the file
                        with open(avoided_songs_file_path, 'w') as avoided_file:
                            json.dump(avoided_songs, avoided_file, indent=4)

                # Ensure the directories exist
                os.makedirs(moved_meta_file_path, exist_ok=True)
                os.makedirs(moved_lyrics_file_path, exist_ok=True)
                
                # Move the processed file to the converted path
                shutil.move(meta_file_path, os.path.join(moved_meta_file_path, os.path.basename(meta_file_path)))
                shutil.move(lyrics_file_path, os.path.join(moved_lyrics_file_path, os.path.basename(lyrics_file_path)))

            except SongNotFoundException as e:
                print(e)
                annot = None
                new_avoided_song_key = f"{title} - {artists[0]}"
                new_avoided_song = {new_avoided_song_key : [metadata_file.split('.')[0],'not_found_on_Genius']}
                if new_avoided_song_key not in avoided_songs:
                    # Append the new entry
                    avoided_songs.update(new_avoided_song)

                    # Save the updated dictionary back to the file
                    with open(avoided_songs_file_path, 'w') as avoided_file:
                        json.dump(avoided_songs, avoided_file, indent=4)

                # Ensure the directories exist
                os.makedirs(moved_meta_file_path, exist_ok=True)
                os.makedirs(moved_lyrics_file_path, exist_ok=True)

                # Move the processed file to the converted path
                shutil.move(meta_file_path, os.path.join(moved_meta_file_path, os.path.basename(meta_file_path)))
                shutil.move(lyrics_file_path, os.path.join(moved_lyrics_file_path, os.path.basename(lyrics_file_path)))
                return f"Success: {metadata_file}"
            
        else:
                new_avoided_song_key = f"{title} - {artists[0]}"
                new_avoided_song = {new_avoided_song_key : [metadata_file.split('.')[0],'notes_encoding_instead_of_lines']}
                if new_avoided_song_key not in avoided_songs:
                    # Append the new entry
                    avoided_songs.update(new_avoided_song)

                    # Save the updated dictionary back to the file
                    with open(avoided_songs_file_path, 'w') as avoided_file:
                        json.dump(avoided_songs, avoided_file, indent=4)
                
                # Ensure the directories exist
                os.makedirs(moved_meta_file_path, exist_ok=True)
                os.makedirs(moved_lyrics_file_path, exist_ok=True)
        
                # Move the processed file to the converted path
                shutil.move(meta_file_path, os.path.join(moved_meta_file_path, os.path.basename(meta_file_path)))
                shutil.move(lyrics_file_path, os.path.join(moved_lyrics_file_path, os.path.basename(lyrics_file_path)))
                return f"Success: {metadata_file}"
    
    except Exception as ex:
        return f"Error processing {metadata_file}: {ex}"

    
def process_dali_file(metadata_file, DALI_dir, save_path, already_converted_path, id_file_path, avoided_songs_file_path):
    try:
        # Get track metadata
        file_path = f"{DALI_dir}{metadata_file.split('.')[0]}.json"

        # Load the existing dictionary of avoided songs from the file
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
        try:
            annot = LyricsAnnot(title, artists[0])
            if not(annot.language in asian_languages or annot.language==None):
                annot.build_annotations(data, 'DALI')
                success = annot.add_section_info()
                
                if success: # song has paragraphs on Genius
                    annot.save_to_json(save_path, id_file_path, 'DALI')
                
                else:
                    new_avoided_song_key = f"{title} - {artists[0]}"
                    new_avoided_song = {new_avoided_song_key : [data['info']['id'],'no_paragraphs']}
                    if new_avoided_song_key not in avoided_songs:
                        # Append the new entry
                        avoided_songs.update(new_avoided_song)

                        # Save the updated dictionary back to the file
                        with open(avoided_songs_file_path, 'w') as avoided_file:
                            json.dump(avoided_songs, avoided_file, indent=4)

            elif annot.language in asian_languages:
                new_avoided_song_key = f"{title} - {artists[0]}"
                new_avoided_song = {new_avoided_song_key : [data['info']['id'],'wrongly_encoded_asian_song']}
                if new_avoided_song_key not in avoided_songs:
                    # Append the new entry
                    avoided_songs.update(new_avoided_song)

                    # Save the updated dictionary back to the file
                    with open(avoided_songs_file_path, 'w') as avoided_file:
                        json.dump(avoided_songs, avoided_file, indent=4)

            elif annot.language==None:
                new_avoided_song_key = f"{title} - {artists[0]}"
                new_avoided_song = {new_avoided_song_key : [data['info']['id'],'no_language_information']}
                if new_avoided_song_key not in avoided_songs:
                    # Append the new entry
                    avoided_songs.update(new_avoided_song)

                    # Save the updated dictionary back to the file
                    with open(avoided_songs_file_path, 'w') as avoided_file:
                        json.dump(avoided_songs, avoided_file, indent=4)
        except SongNotFoundException as e:
                print(e)
                annot = None
                new_avoided_song_key = f"{title} - {artists[0]}"
                new_avoided_song = {new_avoided_song_key : [data['info']['id'],'not_found_on_Genius']}
                if new_avoided_song_key not in avoided_songs:
                    # Append the new entry
                    avoided_songs.update(new_avoided_song)

                    # Save the updated dictionary back to the file
                    with open(avoided_songs_file_path, 'w') as avoided_file:
                        json.dump(avoided_songs, avoided_file, indent=4)
                # Move the processed file to the converted path
                shutil.move(file_path, os.path.join(already_converted_path, os.path.basename(file_path)))
                return f"Success: {metadata_file}"
        
        # Move the processed file to the converted path
        shutil.move(file_path, os.path.join(already_converted_path, os.path.basename(file_path)))
        return f"Success: {metadata_file}"            

    except Exception as ex:
        return f"Error processing {metadata_file}: {ex}"
    

def create_damp_notations(DAMP_dir, save_path, already_converted_path, id_file_path, avoided_songs_file_path, batch_size=10, pause_interval=30, pause_duration=60):
    contents = os.listdir(save_path)
    if not contents : # the folder is empty, no song has been converted yet
        utils.create_id_list(save_path, id_file_path, 'DAMP')
    else:
        if not(utils.check_id_list(save_path, id_file_path)):
            return "The number of IDs of songs successfully converted listed in id.txt is different from the number of files in the folder of the converted songs (./saved). Please fill in id.txt with the songs missing before proceeding with the conversion."
    lan_dirs = os.listdir(DAMP_dir)
    for dir in lan_dirs:
        print(f"Creating notations for {dir} language")
        metadata_files = os.listdir(f"{DAMP_dir}{dir}/{dir}ArrangementMeta/")
        
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            futures = []
            processed_count = 0
            
            for metadata_file in metadata_files:
                futures.append(executor.submit(process_damp_metadata_file, metadata_file, dir, DAMP_dir, save_path, already_converted_path, id_file_path, avoided_songs_file_path))
                processed_count += 1

                # If the number of processed futures is a multiple of the pause interval, pause the execution
                if processed_count % pause_interval == 0:
                    print(f"Processed {processed_count} files, pausing for {pause_duration} seconds...")
                    time.sleep(pause_duration)
            
            for future in tqdm(as_completed(futures), total=len(metadata_files)):
                result = future.result()
                print(result)
    
def create_dali_notations(DALI_dir, save_path, already_converted_path, id_file_path, avoided_songs_file_path, batch_size=10, pause_interval=30, pause_duration=60):
    contents = os.listdir(save_path)
    if not contents : # the folder is empty, no song has been converted yet
        utils.create_id_list(save_path, id_file_path, 'DALI')
    else:
        if not(utils.check_id_list(save_path, id_file_path)):
            return "The number of IDs of songs successfully converted listed in id.txt is different from the number of files in the folder of the converted songs (./saved). Please fill in id.txt with the songs missing before proceeding with the conversion."
    lan_files = os.listdir(DALI_dir)
    for file in lan_files:
        print(f"Creating notations for the file {file}")
        
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            futures = []
            processed_count = 0
            
            futures.append(executor.submit(process_dali_file, file, DALI_dir, save_path, already_converted_path, id_file_path, avoided_songs_file_path))
            processed_count += 1

            # If the number of processed futures is a multiple of the pause interval, pause the execution
            if processed_count % pause_interval == 0:
                print(f"Processed {processed_count} files, pausing for {pause_duration} seconds...")
                time.sleep(pause_duration)
            
            for future in tqdm(as_completed(futures), total=len(lan_files)):
                result = future.result()
                print(result)
    

def main():
    # Adapt it to your use case
    DAMP_dir = "./data/DAMP_MVP/sing_300x30x2/"
    DALI_dir = "./dali/dali_json/"
    save_path = "./conversion/saved"
    dali_already_converted_path = "./dali/dali_already_converted/"
    damp_already_converted_path = "./data/DAMP_MVP/damp_already_converted/"
    id_file_path = "./conversion/id.txt"
    avoided_songs_file_path = "./conversion/avoided_songs.txt"
    # DALI NOTATIONS
    create_dali_notations(DALI_dir, save_path, dali_already_converted_path, id_file_path, avoided_songs_file_path, batch_size=10, pause_interval=30, pause_duration=60)
    # DAMP NOTATIONS
    create_damp_notations(DAMP_dir, save_path, damp_already_converted_path, id_file_path, avoided_songs_file_path, batch_size=10, pause_interval=30, pause_duration=60)
            

if __name__ == '__main__':
    main()