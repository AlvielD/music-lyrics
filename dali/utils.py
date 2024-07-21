from collections import defaultdict

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