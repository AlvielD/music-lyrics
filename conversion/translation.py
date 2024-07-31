from unidecode import unidecode
from googletrans import Translator
from header_synonyms import header_synonyms

# Initialize the translator
translator = Translator()

# Translate synonyms to multiple languages
# TODO: remove languages not used
languages = [
    'af', 'ar', 'az', 'ceb', 'cs', 'da', 'de', 'en', 'es', 'fa', 'fi', 'fr', 'ha', 
    'haw', 'hi', 'hr', 'hu', 'id', 'it', 'ja', 'ko', 'la', 'lv', 'ms', 'nl', 'no', 
    'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'sq', 'sv', 'sw', 'th', 'tr', 'vi', 'xh', 
    'zh', 'zu'
]


def translate_header(header, language):
    normalized_header = unidecode(header).lower().replace('-', ' ')

    # Check in the specified language
    if language in header_synonyms:
        for section, synonyms in header_synonyms[language].items():
            for synonym in synonyms:
                normalized_synonym = unidecode(synonym).lower().replace('-', ' ')
                if normalized_synonym == normalized_header:
                    return section
    else : # not supported language
        return 1

    # Check in English as a fallback
    if 'en' in header_synonyms:
        for section, synonyms in header_synonyms['en'].items():
            for synonym in synonyms:
                normalized_synonym = unidecode(synonym).lower().replace('-', ' ')
                if normalized_synonym == normalized_header:
                    return section

    # If no match is found
    return 0