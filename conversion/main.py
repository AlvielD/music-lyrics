import json
import os
import re
import utils
import time

from GeniusCompiler import GeniusCompiler
from SpotiScraper import SpotiScraper
from LyricsAnnot import LyricsAnnot

from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm

def process_damp_metadata_file(metadata_file, dir, DAMP_dir, save_path):
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
                annot.save_to_json(save_path)
        
        return f"Success: {metadata_file}"
    except Exception as ex:
        return f"Error processing {metadata_file}: {ex}"

    
def process_dali_file(metadata_file, DALI_dir, save_path):
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
        
        # Create annotations
        annot = LyricsAnnot(title, artists[0])
        annot.build_annotations(data, 'DALI')
        success = annot.add_section_info()
            
        if success:
            annot.save_to_json(save_path)
        
        return f"Success: {metadata_file}"
    except Exception as ex:
        return f"Error processing {metadata_file}: {ex}"
    

def create_damp_notations(DAMP_dir, save_path, batch_size=10, pause_interval=30, pause_duration=60):
    lan_dirs = os.listdir(DAMP_dir)
    for dir in lan_dirs:
        print(f"Creating notations for {dir} language")
        metadata_files = os.listdir(f"{DAMP_dir}{dir}/{dir}ArrangementMeta/")
        
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            futures = []
            processed_count = 0
            
            for metadata_file in metadata_files:
                futures.append(executor.submit(process_damp_metadata_file, metadata_file, dir, DAMP_dir, save_path))
                processed_count += 1

                # If the number of processed futures is a multiple of the pause interval, pause the execution
                if processed_count % pause_interval == 0:
                    print(f"Processed {processed_count} files, pausing for {pause_duration} seconds...")
                    time.sleep(pause_duration)
            
            for future in tqdm(as_completed(futures), total=len(metadata_files)):
                result = future.result()
                print(result)
    
def create_dali_notations(DALI_dir, save_path, batch_size=10, pause_interval=30, pause_duration=60):
    lan_files = os.listdir(DALI_dir)
    for file in lan_files:
        print(f"Creating notations for the file {file}")
        
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            futures = []
            processed_count = 0
            
            futures.append(executor.submit(process_dali_file, file, DALI_dir, save_path))
            processed_count += 1

            # If the number of processed futures is a multiple of the pause interval, pause the execution
            if processed_count % pause_interval == 0:
                print(f"Processed {processed_count} files, pausing for {pause_duration} seconds...")
                time.sleep(pause_duration)
            
            for future in tqdm(as_completed(futures), total=len(lan_files)):
                result = future.result()
                print(result)


def main():

    DAMP_dir = "./data/toy_DAMP/"
    #DAMP_dir = "./data/DAMP_MVP/sing_300x30x2/"
    DALI_dir = "./dali/dali_json/"

    save_path = "./conversion/saved"

    # DAMP NOTATIONS
    lan_dirs = os.listdir(DAMP_dir)
    for dir in lan_dirs:
        print(f"Creating notations for {dir} language")
        metadata_files = os.listdir(f"{DAMP_dir}{dir}/{dir}ArrangementMeta/")
        for i, metadata_file in zip(tqdm(range(len(metadata_files))), metadata_files):
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

                annot = LyricsAnnot(title, artists[0])
                annot.build_annotations(data, 'DAMP')
                success = annot.add_section_info()
                
                if success:
                    annot.save_to_json(save_path)
            except Exception as ex:
                print(ex)
    
    # DALI NOTATIONS
    lan_dirs = os.listdir(DALI_dir)
    for file in lan_dirs:
        print(f"Creating notations for the file {file}")
        for i, file in zip(tqdm(range(len(lan_dirs))), lan_dirs):
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
                data = utils.clean_dali_json(data)

                annot = LyricsAnnot(title, artists[0])
                annot.build_annotations(data, 'DAMP')
                success = annot.add_section_info()
                
                if success:
                    annot.save_to_json(save_path)
            except Exception as ex:
                print(ex)

if __name__ == '__main__':
    #main()
    #DAMP_dir = "./data/DAMP_MVP/sing_300x30x2/"
    DALI_dir = "../dali/dali_json/"
    save_path = "./saved/dali/"
    metadata_file = "my_annot_name_022411a432334ca2800c07dfc81848a2.json"
    process_dali_file(metadata_file, DALI_dir, save_path)
    #create_dali_notations(DALI_dir, save_path)