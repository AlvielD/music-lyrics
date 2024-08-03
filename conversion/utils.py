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


def remove_from_paragraph(line, paragraph):
    # Split the line into words
    line_words = line.split()
    # Iterate over the words in the line and create a regex pattern
    pattern = ''
    for word in line_words:
        if re.search(re.escape(word), paragraph):
            pattern += f'{re.escape(word)} '
        else:
            break
    # Remove the trailing space
    pattern = pattern.strip()
    # Find the first matching substring in the paragraph
    match = re.search(pattern, paragraph)
    if match:
        matching_substring = match.group(0)
        
        # Remove the matching substring from the paragraph
        new_paragraph = paragraph.replace(matching_substring, '', 1)
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

def count_specific_sources(file_path):
    try:
        # Load the JSON content from the file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        count = 0
        # Iterate through each key-value pair in the dictionary
        for key, value in data.items():
            sources = value[1]
            # Check if the source list contains both "DALI" and "DAMP" in any order
            if sorted(sources) == ["DALI", "DAMP"]:
                count += 1
        
        return count

    except Exception as ex:
        return f"Error processing the file: {ex}"



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


def update_id_list(save_path, id_file_path, source="Unknown"):
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
    

def correct_time_durations(json_dir):
    try:
        # Iterate through each file in the json_dir directory
        for filename in os.listdir(json_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(json_dir, filename)
                
                # Load the JSON file content
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    
                    # Iterate through each paragraph in the annotations array
                    for paragraph in data.get('annotations', []):
                        # Calculate the correct time_duration
                        time_index = paragraph.get('time_index', [])
                        if len(time_index) == 2:
                            paragraph['time_duration'] = time_index[1] - time_index[0]
                    
                    # Save the updated JSON back to the file
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(data, file, indent=4)
        
        return "Time durations corrected successfully."

    except Exception as ex:
        return f"Error correcting time durations: {ex}"


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



def count_avoided_songs(avoided_songs_file_path):
    try:
        # Load the JSON content from the file
        with open(avoided_songs_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Initialize counters
        dali_counts = {
            "no_language_information": 0,
            "wrongly_encoded_asian_song": 0,
            "no_paragraphs": 0,
            "not_found_on_Genius": 0,
            "total": 0
        }
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
            
            # Determine dataset and increment corresponding counter
            if "_" in song_id: #DAMP
                if reason == "no_language_information":
                    damp_counts["no_language_information"] += 1
                elif reason == "notes_encoding_instead_of_lines":
                    damp_counts["notes_encoding_instead_of_lines"] += 1
                elif reason == "no_paragraphs":
                    damp_counts["no_paragraphs"] += 1
                elif reason == "not_found_on_Genius":
                    damp_counts["not_found_on_Genius"] += 1
                damp_counts["total"] = damp_counts["no_language_information"]+damp_counts["notes_encoding_instead_of_lines"]+damp_counts["no_paragraphs"]+damp_counts["not_found_on_Genius"]
            else: #DALI
                if reason == "no_language_information":
                    dali_counts["no_language_information"] += 1
                elif reason == "wrongly_encoded_asian_song":
                    dali_counts["wrongly_encoded_asian_song"] += 1
                elif reason == "no_paragraphs":
                    dali_counts["no_paragraphs"] += 1
                elif reason == "not_found_on_Genius":
                    dali_counts["not_found_on_Genius"] += 1
                dali_counts["total"] = dali_counts["no_language_information"]+dali_counts["wrongly_encoded_asian_song"]+dali_counts["no_paragraphs"]+dali_counts["not_found_on_Genius"]

        
        return {"dali_counts": dali_counts, "damp_counts": damp_counts}

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