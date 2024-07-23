import pylcs
import re
import unicodedata

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


if __name__ == '__main__':
    pass