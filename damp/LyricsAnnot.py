import utils
import json
import SpotiScraper as SpotiScraper
from pprint import pprint

class LyricsAnnot:
    _last_id = 0
    _id_len = 8

    # Maximum value for the given length in hexadecimal
    _max_id = int("F" * _id_len, 16)

    _spoti_client = SpotiScraper.SpotiScraper()

    def __init__(self, title = None, artist = None):
        # Meta-data attributes
        self.song_id = self.build_id()
        self.title = title
        self.artist = artist

        # Define attributes dependant on title and signer
        if title and artist:
            self.language = utils.get_song_langugage(title, artist)
            self.song_duration = LyricsAnnot._spoti_client.get_song_duration(title, artist)
        else:
            self.language = None
            self.song_duration = None

        self.annotations = []

    
    def set_song_metadata(self, title, artist):
        self.title = title
        self.artist = artist
        self.language = utils.get_song_langugage(title, artist)
        self.song_duration = LyricsAnnot._spoti_client.get_song_duration(title, artist)


    def build_id(self):
        """Build the id of the song from the class attributes

        Raises:
            ValueError: If the maximum ID was reached

        Returns:
            str: string representation of the song's ID
        """
        if LyricsAnnot._last_id >= LyricsAnnot._max_id:
            raise ValueError(f"Maximum ID value of {'F' * LyricsAnnot._id_length} reached.")
        
        song_id = f"{LyricsAnnot._last_id:0{LyricsAnnot._id_len}X}"
        LyricsAnnot._last_id += 1

        return song_id

    
    def build_annotations(self, data, dataset = 'DAMP'):
        try:
            if data:
                if dataset == 'DAMP':
                    annotations = [{
                        'line': data[i]['l'],
                        'time_index': [data[i]['t'], data[i+1]['t'] - 0.1],
                        'time_duration': data[i+1]['t'] - data[i]['t']} for i in range(len(data)-1)]
                    annotations.append({
                        'line': data[-1]['l'],
                        'time_index': [data[-1]['t'], self.song_duration],
                        'time_duration': self.song_duration - data[-1]['t']})
                    
                    self.annotations = annotations
                    print("Annotations built succesfully!")
                elif dataset == 'DALI':
                    # TODO: Add here procedure to build DALI annotations
                    pass
                else:
                    print("Dataset not supported. Annotations were not built.")
            else:
                print("Data was not provided.")

            return True
        except Exception:
            print("Annotations were not built.")
            return False
        

    def save_to_json(self):
        data = {
            'meta': {
                'song_id': self.song_id,
                'title': self.title,
                'artist': self.artist,
                'language': self.language
            },
            'annotations': self.annotations
        }

        with open(f'./saved/{self.song_id}.json', 'w') as file:
            json.dump(data, file, indent=4)
        

    def print_song(self):
        print("META-DATA")
        print("------------------------")
        print(f"ID:\t{self.song_id}")
        print(f"Title:\t{self.title}")
        print(f"Artist:\t{self.artist}")
        print(f"Lang:\t{self.language}")
        print(f"Duration:\t{self.song_duration}\n")

        print("ANNOTATIONS")
        print("------------------------")
        pprint(self.annotations)

