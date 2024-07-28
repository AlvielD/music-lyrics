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