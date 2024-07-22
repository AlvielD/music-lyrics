import json

from GeniusCompiler import GeniusCompiler
from SpotiScraper import SpotiScraper
from LyricsAnnot import LyricsAnnot

def main():

    title = 'Perro fiel'
    artist = 'Shakira'

    # READ AUDIO-ALIGNED ADATA AND INSTANTIATE A LYRICS ANNOTATION OBJECT
    file_path = './data/DAMP_MVP/sing_300x30x2/ES/ESLyrics/3364824_3364824.json'

    with open(file_path, encoding='utf-8') as file:
        data = json.load(file)

    annot = LyricsAnnot(title, artist)
    annot.build_annotations(data, 'DAMP')
    annot.add_section_info()
    
    print(annot)

if __name__ == '__main__':
    main()