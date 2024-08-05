import pylcs
import re
import json
import pprint
import unicodedata
import emoji
import os

from tqdm import tqdm

SPECIAL_CHARS = ["¿", "?", "!", "¡", ":", ";", ",", ".", "\\", "/", "\"", "\'"]

def remove_accents(input_str):
    normalized_str = unicodedata.normalize('NFD', input_str)
    return ''.join(c for c in normalized_str if unicodedata.category(c) != 'Mn')


def remove_special_chars(input_str):
    return ''.join(c for c in input_str if c not in SPECIAL_CHARS)


def compute_similiarity_score(str1, str2):
    str1 = remove_accents(remove_special_chars(str1))
    str2 = remove_accents(remove_special_chars(str2))

    try:
        score = pylcs.lcs_string_length(str1.lower(), str2.lower()) / len(str1)
    except ZeroDivisionError:
        score = 0.0

    return score


def normalize_text(text):
    # Normalize curly quotes and other special characters
    text = text.replace('’', "'").replace('“', '"').replace('”', '"')
    # Normalize multiple spaces to a single space
    text = re.sub(r'\s+', ' ', text)
    return text.lower().strip()

def remove_leading_punctuation(text):
    # Define the set of punctuation characters to remove at the start
    # Exclude characters that might be valid at the start of a line in some languages
    punctuation = r'^[,.\s?!;:\'"]+'
    # Remove leading punctuation and spaces
    cleaned_text = re.sub(punctuation, '', text)
    return cleaned_text


def remove_from_paragraph(line, paragraph):
    # Normalize both line and paragraph
    normalized_paragraph = normalize_text(paragraph)
    normalized_line = normalize_text(line)

    # Split the line into words
    line_words = normalized_line.split()
    
    # Construct a regex pattern to match the entire line as a sequence of words
    pattern = r'\s*'.join(re.escape(word) for word in line_words)

    # Find the first matching substring in the paragraph
    match = re.search(pattern, normalized_paragraph)
    if match:
        matching_substring = match.group(0)
        
        # Remove the matching substring from the paragraph using span
        start, end = match.span()
        new_paragraph = paragraph[end:]
        # Remove leading punctuation and spaces
        new_paragraph = remove_leading_punctuation(new_paragraph)
        return new_paragraph
    else:
        return paragraph
    

def startswith_similar(line, paragraph, threshold=0.6):
    """
    Checks if the paragraph content starts similarly to the line text with a given similarity threshold.
    
    Args:
        paragraph_content (str): The content of the paragraph.
        line_text (str): The text to compare with the start of the paragraph.
        threshold (float): The similarity threshold above which the strings are considered to start similarly.
        
    Returns:
        bool: True if the start of the paragraph is similar to the line text based on the threshold, False otherwise.
    """
    # Compare only the beginning of the paragraph content up to the length of the line text
    start_content = paragraph[:len(line)]
    similarity_score = compute_similiarity_score(line, start_content)

    return similarity_score >= threshold


def clean_damp_json(lines):

    n_lines = len(lines)

    front_index = -1
    for i in range(n_lines):
        if contains_any_char(lines[i], 'DAMP'):
            front_index = i
        if i/n_lines > .2:
            break

    back_index = n_lines
    for i in range(n_lines-1, -1, -1):
        if contains_any_char(lines[i], 'DAMP'):
            back_index = i
        if i/n_lines < .8:
            break

    print(f"DETECTED FRONT INDEX: {front_index}")
    print(f"DETECTED BACK INDEX {back_index}")

    return lines[front_index+1:back_index]

def clean_dali_json(lines):

    n_lines = len(lines)

    front_index = -1
    for i in range(n_lines):
        if contains_any_char(lines[i]['text'], 'DALI'):
            front_index = i
        if i/n_lines > .2:
            break

    back_index = n_lines
    for i in range(n_lines-1, -1, -1):
        if contains_any_char(lines[i]['text'], 'DALI'):
            back_index = i
        if i/n_lines < .8:
            break

    print(f"DETECTED FRONT INDEX: {front_index}")
    print(f"DETECTED BACK INDEX {back_index}")

    return lines[front_index+1:back_index]


def contains_any_char(sample, dataset):
    if dataset == 'DAMP':
        pattern = r"(?i)[#@><_&^=•]|-.*-|follow|upload|song by|thank|thumbs|\.{4,}"
        return True if re.search(pattern, sample['l'].lower()) or contains_emoji(sample['l'].lower()) else False
    if dataset == 'DALI':
        pattern = r"(?i)[#@><_&^=•]|-.*-|follow|upload|song by|thank|thumbs|\.{4,}"
        return True if re.search(pattern, sample.lower()) or contains_emoji(sample.lower()) else False


def contains_emoji(text):
    return any(char in emoji.EMOJI_DATA for char in text)


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

def compute_avg_line_len(lines):
    avg_len = 0
    n_line = len(lines)
    for line in lines:
        avg_len += len(line['l'])
    avg_len /= n_line
    return avg_len


#---------------FUNCTIONS FOR PRE-CONVERSION---------------
# Check if the text file containing the id of already converted songs is up-to-date compared
# to the actual content of the output folder
# Note: this is a very simple check so as to lower performance needs (number of id must match number of files)
def check_id_list(save_path, id_file_path):
    try:
        # Count the number of files in the save_path directory
        file_count = len([f for f in os.listdir(save_path) if os.path.isfile(os.path.join(save_path, f))])

        # Load the dictionary from the JSON file
        if os.path.exists(id_file_path):
            with open(id_file_path, 'r') as id_file:
                try:
                    id_list = json.load(id_file)
                except json.JSONDecodeError:
                    raise ValueError("The id file contains invalid JSON.")
        else:
            raise FileNotFoundError("The id file does not exist.")

        # Count the number of items in the id_list
        id_count = len(id_list)

        # Check if the file count matches the id count
        if file_count == id_count:
            return True
        else:
            return False

    except Exception as ex:
        return f"Error checking ID list: {ex}"


def create_id_list(save_path, id_file_path, source):
    try:
        # Initialize an empty dictionary
        id_list = {}

        # Iterate through each file in the save_path directory
        for filename in os.listdir(save_path):
            if filename.endswith('.json'):
                file_path = os.path.join(save_path, filename)
                
                # Load the JSON file content
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    
                    # Extract the title, artist, and song_id
                    title = data['meta']['title']
                    artist = data['meta']['artist']
                    song_id = filename.split('.')[0]  # Remove the '.json' extension to get the ID

                    # Create the key as "title - artist"
                    new_id_key = f"{title} - {artist}"
                    
                    # Add to the dictionary
                    id_list[new_id_key] = [song_id, source]

        # Write the dictionary to the id_file_path, overwriting existing content
        with open(id_file_path, 'w') as id_file:
            json.dump(id_list, id_file, indent=4)

        return "ID list updated successfully."

    except Exception as ex:
        return f"Error updating ID list: {ex}"


#---------------FUNCTIONS FOR POST-CONVERSION---------------
# Get the id of songs that got wrongly converted (single paragraphs)
def get_single_paragraph_song_info(folder_path):
    single_paragraph_songs = {}

    # Loop through all files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            
            # Open and read the JSON file
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    
                    # Check if the JSON file has only one paragraph
                    if 'annotations' in data and len(data['annotations']) == 1:
                        song_id = data['meta']['song_id']
                        title = data['meta']['title']
                        artist = data['meta']['artist']
                        single_paragraph_songs[song_id] = (title, artist)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {file_path}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred with file {file_path}: {e}")
    
    return single_paragraph_songs


# Function to delete the songs with single paragraphs from the id file
def delete_dict_entries(files_dict, dict_path):
    # Load the dictionary from the given file path
    with open(dict_path, 'r') as file:
        dictionary = json.load(file)

    print(f"Initial dictionary size: {len(dictionary)}")

    # Keep track of the last matched index
    last_index = 0

    for file_id in files_dict.keys():
        keys = list(dictionary.keys())
        for i in range(last_index, len(keys)):
            key = keys[i]
            if dictionary[key][0] == file_id:
                del dictionary[key]
                last_index = i
                break  # Assuming file ID matches only one entry, break the loop

    print(f"Dictionary size after deletions: {len(dictionary)}")

    # Save the updated dictionary back to the file
    with open(dict_path, 'w') as json_file:
        json.dump(dictionary, json_file, indent=4)


# Function to recompute IDs and rename files
def delete_wrong_converted_songs(files_dict, files_directory):
    for key in list(files_dict.keys()):
        # Find the matching file and delete it
        for file in os.listdir(files_directory):
            filename = os.path.splitext(file)[0]
            if filename == key:
                path_to_delete = os.path.join(files_directory, file)
                os.remove(path_to_delete)
                break
        
# Function to recompute IDs and rename files
def change_ids_and_rename_files(dict_path, files_directory, id_len):
    # Load the dictionary from the given file path
    with open(dict_path, 'r') as file:
        dictionary = json.load(file)
    
    new_dict = {}
    new_id_counter = 0

    for key in list(dictionary.keys()):
        # Get the old entry
        old_id = dictionary[key][0]
        source = dictionary[key][1]

        # Format the new ID with the given length
        new_id = f"{new_id_counter:0{id_len}X}"
        
        if old_id == new_id:
            new_dict[key] = [old_id, source]
        else:
            new_dict[key] = [new_id, source]

            # Find the matching file
            old_file = None
            for file in os.listdir(files_directory):
                filename = os.path.splitext(file)[0]
                if filename == old_id:
                    old_file = file
                    break
            
             # Rename the file with the new ID if found
            if old_file:
                new_file = f"{new_id}{os.path.splitext(old_file)[1]}"
                old_path = os.path.join(files_directory, old_file)
                new_path = os.path.join(files_directory, new_file)
                os.rename(old_path, new_path)

                # Open the JSON file and update the id field
                with open(new_path, 'r') as json_file:
                    data = json.load(json_file)
                
                data['meta']['song_id'] = new_id

                with open(new_path, 'w') as json_file:
                    json.dump(data, json_file, indent=4)

        new_id_counter += 1  # Increment the counter instead of resetting it

    # Save the updated dictionary back to the file
    with open(dict_path, 'w') as file:
        json.dump(new_dict, file, indent=4)


#---------------FUNCTIONS FOR STATISTICS---------------
def count_sources(id_file_path):
    try:
        # Load the JSON content from the file
        with open(id_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        count_dali = 0
        count_damp = 0
        count_double_sources = 0
        # Iterate through each key-value pair in the dictionary
        for key, value in data.items():
            sources = value[1]
            # Check if the source list contains both "DALI" and "DAMP" in any order
            if "DALI" in sources and "DAMP" in sources:
                count_double_sources += 1
                count_dali += 1
                count_damp += 1
            else:
                if "DALI" in sources:
                    count_dali += 1
                if "DAMP" in sources:
                    count_damp += 1
        
        return {"count_dali":count_dali, "count_damp":count_damp, "count_double_sources":count_double_sources}

    except Exception as ex:
        return f"Error processing the file: {ex}"

    
def count_files(folder_path):
    try:
        # List all files in the directory
        files = os.listdir(folder_path)
        # Filter out directories, only count files
        files_count = len([f for f in files if os.path.isfile(os.path.join(folder_path, f))])
        return files_count
    except Exception as ex:
        print(f"Error counting files in {folder_path}: {ex}")
        return 0

def calculate_percentage(id_file_path, dataset_already_converted, dataset):
    try:
        source_counts = count_sources(id_file_path)
        if dataset == "DALI":
            converted_count=source_counts["count_dali"]
        if dataset == "DAMP":
            converted_count=source_counts["count_damp"]
        
        total_count = count_files(dataset_already_converted)

        if total_count == 0:
            return "Cannot calculate percentage because no file has been processed yet."

        percentage = (converted_count / total_count) * 100
        return f"{percentage:.2f}% of the songs from {dataset} dataset are usable to create the feed the knowledge graph."
    
    except Exception as ex:
        return f"Error calculating percentage: {ex}"



def dali_count_avoided_songs(dali_avoided_songs_file_path):
    try:
        # Load the JSON content from the file
        with open(dali_avoided_songs_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Initialize counters
        dali_counts = {
            "no_language_information": 0,
            "wrongly_encoded_asian_song": 0,
            "no_paragraphs": 0,
            "not_found_on_Genius": 0,
            "total": 0
        }
        
        # Iterate through each key-value pair in the dictionary
        for key, value in data.items():
            song_id = value[0]
            reason = value[1]
            if reason == "no_language_information":
                dali_counts["no_language_information"] += 1
            elif reason == "wrongly_encoded_asian_song":
                dali_counts["wrongly_encoded_asian_song"] += 1
            elif reason == "no_paragraphs":
                dali_counts["no_paragraphs"] += 1
            elif reason == "not_found_on_Genius":
                dali_counts["not_found_on_Genius"] += 1
            dali_counts["total"] = dali_counts["no_language_information"]+dali_counts["wrongly_encoded_asian_song"]+dali_counts["no_paragraphs"]+dali_counts["not_found_on_Genius"]

        
        return {"dali_counts": dali_counts}

    except Exception as ex:
        return f"Error processing the file: {ex}"
    

def damp_count_avoided_songs(damp_avoided_songs_file_path):
    try:
        # Load the JSON content from the file
        with open(damp_avoided_songs_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Initialize counters
        damp_counts = {
            "no_language_information": 0,
            "notes_encoding_instead_of_lines": 0,
            "no_paragraphs": 0,
            "not_found_on_Genius": 0,
            "total": 0
        }
        
        # Iterate through each key-value pair in the dictionary
        for key, value in data.items():
            song_id = value[0]
            reason = value[1]
            if reason == "no_language_information":
                damp_counts["no_language_information"] += 1
            elif reason == "notes_encoding_instead_of_lines":
                damp_counts["notes_encoding_instead_of_lines"] += 1
            elif reason == "no_paragraphs":
                damp_counts["no_paragraphs"] += 1
            elif reason == "not_found_on_Genius":
                damp_counts["not_found_on_Genius"] += 1
            damp_counts["total"] = damp_counts["no_language_information"]+damp_counts["notes_encoding_instead_of_lines"]+damp_counts["no_paragraphs"]+damp_counts["not_found_on_Genius"]

        
        return {"damp_counts": damp_counts}

    except Exception as ex:
        return f"Error processing the file: {ex}"




if __name__ == '__main__':

    """
    toy_DAMP = "./data/toy_DAMP/"

    lan_dirs = os.listdir(toy_DAMP)
    for dir in lan_dirs:
        metadata_files = os.listdir(f"{toy_DAMP}{dir}/{dir}ArrangementMeta/")
        for i, metadata_file in zip(tqdm(range(len(metadata_files))), metadata_files):
            # Get track metadata from the metadata file
            track_metadata = read_arrangement_file(f"{toy_DAMP}{dir}/{dir}ArrangementMeta/{metadata_file}")

            title = parse_title(track_metadata['Arrangement title'])
            artists = parse_artist_names(track_metadata['Arrangement artist'])

            file_path = f"{toy_DAMP}{dir}/{dir}Lyrics/{metadata_file.split('.')[0]}.json"

            # Read JSON file
            with open(file_path, encoding='utf-8') as file:
                data = json.load(file)

            lyrics = clean_json(data)
            pprint.pprint(lyrics)
    """
    with open('./data/DAMP_MVP/sing_300x30x2/AE/AELyrics/3770008_3770008.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    print(compute_avg_line_len(data))