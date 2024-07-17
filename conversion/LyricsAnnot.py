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

        # Define attributes dependant on title and singer
        if title and artist:
            self.language = utils.get_song_language(title, artist)
            #self.song_writers = LyricsAnnot._spoti_client.get_song_writers(title, artist)
            self.song_duration = LyricsAnnot._spoti_client.get_song_duration(title, artist)
        else:
            self.language = None
            self.song_duration = None

        self.annotations = []

    
    def set_song_metadata(self, title, artist):
        self.title = title
        self.artist = artist
        self.language = utils.get_song_language(title, artist)
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


    # TODO: Check this method (sometimes it skips lines)
    def add_section_info(self, genius_data):

        merged_annotations = []

        # Initialize variables to track current paragraph and its content
        current_paragraph_name = None
        current_paragraph_content = None
        current_paragraph_start_time = None
        current_paragraph_end_time = None
        
        # Iterate through annotation lines
        for line in self.annotations:
            line_text = line['line']
            line_start_time = line['time_index'][0]
            line_end_time = line['time_index'][1]
            
            # Check if current line belongs to the current paragraph
            if current_paragraph_content and line_text in current_paragraph_content:
                # Add line information to current paragraph
                lines = {
                    'line': line_text,
                    'time_index': [line_start_time, line_end_time],
                    'time_duration': line_end_time - line_start_time
                }
                merged_annotations[-1]['lines'].append(lines)
                
                # Update current paragraph end time
                current_paragraph_end_time = line_end_time
            else:
                # If current line doesn't belong to current paragraph, finalize current paragraph
                if current_paragraph_name:
                    merged_annotations[-1]['time_index'] = [current_paragraph_start_time, current_paragraph_end_time]
                
                # Move to a new paragraph section
                for paragraph_name, paragraph_info in genius_data.items():
                    paragraph_content = paragraph_info['content']
                    singer = paragraph_info['singer']
                    
                    # Check if current line starts a new paragraph
                    if paragraph_content.startswith(line_text):
                        # Initialize new paragraph
                        current_paragraph_name = paragraph_name
                        current_paragraph_content = paragraph_content
                        current_paragraph_start_time = line_start_time
                        current_paragraph_end_time = line_end_time
                        
                        # Add new annotation for the paragraph
                        annotation_data = {
                            'paragraph': current_paragraph_name,
                            'time_index': [current_paragraph_start_time, current_paragraph_end_time],
                            'time_duration': current_paragraph_end_time - current_paragraph_start_time,
                            'singer': singer,
                            'lines': [{
                                'line': line_text,
                                'time_index': [line_start_time, line_end_time],
                                'time_duration': line_end_time - line_start_time
                            }]
                        }
                        
                        merged_annotations.append(annotation_data)
                        
                        break  # Stop searching for paragraph after finding match

        # Finalize last paragraph if any
        if current_paragraph_name:
            merged_annotations[-1]['time_index'] = [current_paragraph_start_time, current_paragraph_end_time]
        
        # Prepare merged data structure
        self.annotations = merged_annotations
        

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

