from collections import defaultdict
import os

def display_languages(dali_data):
    # Initialize a dictionary to store language counts and IDs
    language_data = defaultdict(lambda: {'count': 0, 'ids': []})

    # Iterate through all files in dali_data
    for key, entry in dali_data.items():
        # Extract the language and ID from each entry
        language = entry.info['metadata']['language']
        file_id = entry.info['id']
        
        # Update the language data
        language_data[language]['count'] += 1
        language_data[language]['ids'].append(file_id)

    # Display the results
    for language, data in language_data.items():
        print(f"Language: {language}")
        print(f"Count: {data['count']}")
        print(f"IDs: {', '.join(data['ids'])}")
        print("------")


def get_all_artists(dali_data):
    artists = set()  # Using a set to avoid duplicate artists

    # Loop through all files in the dataset directory
    for key, entry in dali_data.items():
        # Extract the artist name
        artist = entry.info['artist']
        if artist:
            artists.add(artist)

    # Convert set to list and sort it
    sorted_artists = sorted(artists)
    return sorted_artists