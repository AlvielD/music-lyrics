import json
import pprint

import pylcs

from SpotiScraper import SpotiScraper
from GeniusCompiler import GeniusCompiler

class LyricsAnnot:
    # PRIVATE ATTRIBUTES
    _last_id = 0
    _id_len = 8
    _max_id = int("F" * _id_len, 16)

    _spoti_client = SpotiScraper()
    _genius_compiler = GeniusCompiler()


    def __init__(self, title, artist):
        # Meta-data attributes
        self.song_id = self.__build_id()
        self.title = title
        self.artist = artist

        # Define attributes dependant on external sources
        song_id = LyricsAnnot._genius_compiler.search_song(self.title, self.artist).id
        metadata = LyricsAnnot._genius_compiler.get_song_metadata(song_id)

        self.language = metadata['language']
        self.writer_artists = metadata['writer_artists']
        self.song_duration = LyricsAnnot._spoti_client.get_song_duration(title, artist)

        self.annotations = []


    def __str__(self) -> str:
        annot = "META-DATA\n"
        annot += "------------------------\n"
        annot += f"ID:\t{self.song_id}\n"
        annot += f"Title:\t{self.title}\n"
        annot += f"Artist:\t{self.artist}\n"
        annot += f"Lang:\t{self.language}\n"
        annot += f"Writer Artists:\t{self.writer_artists}\n"
        annot += f"Duration:\t{self.song_duration}\n\n"

        annot += "ANNOTATIONS\n"
        annot += "------------------------\n"
        annot += pprint.pformat(self.annotations)

        return annot


    def __build_id(self):
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
        """Add audio-aligned data from the data provided in json format

        Args:
            data (dict): json data read from file
            dataset (str, optional): dataset from which the data was read, some fields may vary. Defaults to 'DAMP'.

        Returns:
            bool: whether the audio-aligned data was succesfully added
        """
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
                    print("Annotations built successfully!")
                elif dataset == 'DALI':
                    entry = data['annotations']['annot']['lines']
                    annotations = [{
                        'line': entry[i]['text'],
                        'time_index': [entry[i]['time'][0], entry[i]['time'][1]],
                        'time_duration': entry[i]['time'][1] - entry[i]['time'][0]} for i in range(len(entry))]
                    
                    self.annotations = annotations
                    print("Annotations built successfully!")
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

        with open(f'./saved/{self.song_id}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)


    def add_section_info(self):
        """Adds information about song sections (chorus, verse, ...) to the current annotations.
        """
        lyrics = LyricsAnnot._genius_compiler.get_lyrics(self.title, self.artist)
        paragraphs = LyricsAnnot._genius_compiler.split_by_section(lyrics, self.artist)
        self.annotations = self.__merge_annotations(paragraphs)


    def __merge_annotations(self, paragraphs):
        """Merges the current annotations with the paragraphs information provided

        Args:
            paragraphs (_type_): sections information scraped from Genius API

        Returns:
            array: enhanced annotations with sections information.
        """
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
            if current_paragraph_content:
                doc_score = pylcs.lcs_string_length(line_text.lower(), current_paragraph_content.lower()) / len(line_text)
                #print(f"SCORE BETWEEN {line_text} AND {current_paragraph_content}: {doc_score}")
            if current_paragraph_content and doc_score > 0.6:
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

                match = False
                
                # Move to a new paragraph section
                for paragraph_name, paragraph_info in paragraphs.items():
                    paragraph_content = paragraph_info['content']
                    singer = paragraph_info['singer']

                   
                    # Check if current line starts a new paragraph
                    if startswith_similar(paragraph_content, line_text):
                        match = True

                        # Initialize new paragraph
                        current_paragraph_name = paragraph_name
                        current_paragraph_content = paragraph_content
                        current_paragraph_start_time = line_start_time
                        current_paragraph_end_time = line_end_time

                        #print('Match found!')
                        
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
                if match == False:
                    #print('No match found. The line has been added to the current paragraph by default.')
                    lines = {
                        'line': line_text,
                        'time_index': [line_start_time, line_end_time],
                        'time_duration': line_end_time - line_start_time
                    }
                    merged_annotations[-1]['lines'].append(lines)

        # Finalize last paragraph if any
        if current_paragraph_name:
            merged_annotations[-1]['time_index'] = [current_paragraph_start_time, current_paragraph_end_time]
            
        return merged_annotations
    

def startswith_similar(paragraph_content, line_text, threshold=0.6):
    """
    Checks if the paragraph content starts similarly to the line text with a given similarity threshold.
    
    Args:
        paragraph_content (str): The content of the paragraph.
        line_text (str): The text to compare with the start of the paragraph.
        threshold (float): The similarity threshold above which the strings are considered to start similarly.
        
    Returns:
        bool: True if the start of the paragraph is similar to the line text based on the threshold, False otherwise.
    """
    # Convert both strings to lower case for case-insensitive comparison
    paragraph_content = paragraph_content.lower()
    line_text = line_text.lower()
    
    # Compare only the beginning of the paragraph content up to the length of the line text
    start_content = paragraph_content[:len(line_text)]
    
    # Calculate the similarity score using LCS
    similarity_score = pylcs.lcs_string_length(line_text, start_content) / len(line_text)

    #print(similarity_score)
    
    # Check if the similarity score meets the threshold
    return similarity_score >= threshold


if __name__ == '__main__':
    
    # Read the data from a JSON file
    file_path = './data/DAMP_MVP/sing_300x30x2/ES/ESLyrics/3364824_3364824.json'
    with open(file_path, encoding='utf-8') as file:
        data = json.load(file)

    # Create the instance of lyrics annotations
    title = 'Perro fiel'
    artist = 'Shakira'

    annot = LyricsAnnot(title, artist)
    annot.build_annotations(data, 'DAMP')
    annot.add_section_info()

    annot.save_to_json()