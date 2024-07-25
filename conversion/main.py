import json
import os
import re
import utils

from GeniusCompiler import GeniusCompiler
from SpotiScraper import SpotiScraper
from LyricsAnnot import LyricsAnnot

from tqdm import tqdm

def main():

    DAMP_dir = "./data/toy_DAMP/"
    #DAMP_dir = "./data/DAMP_MVP/sing_300x30x2/"
    DALI_dir = "./data/DALI_v1.0/"

    save_path = "./conversion/saved"

    # Save DAMP annotations
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
                data = utils.clean_json(data)

                annot = LyricsAnnot(title, artists[0])
                annot.build_annotations(data, 'DAMP')
                success = annot.add_section_info()
                
                if success:
                    annot.save_to_json(save_path)
            except Exception as ex:
                print(ex)

if __name__ == '__main__':
    main()