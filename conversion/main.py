import json
import os
import re

import asyncio

from GeniusCompiler import GeniusCompiler
from SpotiScraper import SpotiScraper
from LyricsAnnot import LyricsAnnot

def read_arrangement_file(file_path):
    arrangement_data = {}

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if ': ' in line:
                key, value = line.split(': ', 1)
                arrangement_data[key] = value
            else:
                print(f"Skipping line: {line} (does not contain ': ')")

    return arrangement_data


def parse_artist_names(artist_data):
    # Define regex pattern to split the artist names by common delimiters
    pattern = r'\s*&\s*|\s*Ft\.\s*|\s*,\s*'
    
    # Split the artist data based on the pattern
    artists = re.split(pattern, artist_data)

    # Remove leading and trailing whitespaces from each artist name
    artists = [artist.strip() for artist in artists]
    
    return artists

def main():

    toy_DAMP = "./data/toy_DAMP/"
    DAMP_dir = "./data/DAMP_MVP/sing_300x30x2/"
    DALI_dir = "./data/DALI_v1.0/"

    save_path = "./conversion/saved"

    # Save DAMP annotations
    lan_dirs = os.listdir(toy_DAMP)
    for dir in lan_dirs:
        metadata_files = os.listdir(f"{toy_DAMP}{dir}/{dir}ArrangementMeta/")
        for metadata_file in metadata_files:
            try:
                # Get track metadata from the metadata file
                track_metadata = read_arrangement_file(f"{toy_DAMP}{dir}/{dir}ArrangementMeta/{metadata_file}")

                artists = parse_artist_names(track_metadata['Arrangement artist'])

                file_path = f"{toy_DAMP}{dir}/{dir}Lyrics/{metadata_file.split('.')[0]}.json"

                # Read JSON file
                with open(file_path, encoding='utf-8') as file:
                    data = json.load(file)

                annot = LyricsAnnot(track_metadata['Arrangement title'], artists[0])
                annot.build_annotations(data, 'DAMP')
                annot.add_section_info()
                print(annot)
                annot.save_to_json(save_path)
            except:
                print("Song not found")

if __name__ == '__main__':
    main()