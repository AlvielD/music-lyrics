import json
import os
import re

from GeniusCompiler import GeniusCompiler
from SpotiScraper import SpotiScraper
from LyricsAnnot import LyricsAnnot

from tqdm import tqdm

def read_arrangement_file(file_path):
    arrangement_data = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if ': ' in line:
                key, value = line.split(': ', 1)
                arrangement_data[key] = value
            else:
                print(f"Skipping line: {line} (does not contain ': ')")

    return arrangement_data


def parse_title(string):
    no_parentheses = re.sub(r'\([^)]*\)', '', string)               # Use regular expression to remove text within parentheses
    cleaned_string = re.sub(r'\s+', ' ', no_parentheses).strip()    # Remove extra spaces that might result from the removal
    return cleaned_string


def parse_artist_names(string):
    pattern = r'\s*&\s*|\s*Ft\.\s*|\s*,\s*' # Define regex pattern to split the artist names by common delimiters
    artists = re.split(pattern, string)     # Split the artist data based on the pattern    
    artists = [artist.strip() for artist in artists]    # Remove leading and trailing whitespaces from each artist name
    return artists

def main():

    toy_DAMP = "./data/toy_DAMP/"
    DAMP_dir = "./data/DAMP_MVP/sing_300x30x2/"
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
                track_metadata = read_arrangement_file(f"{DAMP_dir}{dir}/{dir}ArrangementMeta/{metadata_file}")

                title = parse_title(track_metadata['Arrangement title'])
                artists = parse_artist_names(track_metadata['Arrangement artist'])

                file_path = f"{DAMP_dir}{dir}/{dir}Lyrics/{metadata_file.split('.')[0]}.json"

                # Read JSON file
                with open(file_path, encoding='utf-8') as file:
                    data = json.load(file)

                annot = LyricsAnnot(title, artists[0])
                annot.build_annotations(data, 'DAMP')
                success = annot.add_section_info()
                
                if success:
                    annot.save_to_json(save_path)
            except Exception as ex:
                print(ex)

if __name__ == '__main__':
    main()