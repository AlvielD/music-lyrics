import json

from GeniusCompiler import GeniusCompiler
from SpotiScraper import SpotiScraper
from LyricsAnnot import LyricsAnnot

def main():
    # READ AUDIO-ALIGNED ADATA AND INSTANTIATE A LYRICS ANNOTATION OBJECT
    file_path = './data/DAMP_MVP/sing_300x30x2/ES/ESLyrics/3364824_3364824.json'

    with open(file_path, encoding='utf-8') as file:
        data = json.load(file)

    annot = LyricsAnnot('Perro fiel', 'Shakira')   # Create the Lyrics object
    annot.build_annotations(data, 'DAMP')          # Build the annotations from the read data and print again

    print(annot)

    # CREATE THE GENIUS COMPILER, GET THE DATA FROM THE WEB AND ADD IT TO THE LYRICS
    compiler = GeniusCompiler()
    genius_data = compiler.get_lyrics('Perro Fiel', 'Shakira')  # Scrape the lyrics from Genius
    paragraphs = compiler.split_by_section(genius_data)         # Split lyrics by sections if present

    annot.add_section_info(paragraphs)                          # Add info about the sections to the annotations
    
    print(annot)

if __name__ == '__main__':
    main()