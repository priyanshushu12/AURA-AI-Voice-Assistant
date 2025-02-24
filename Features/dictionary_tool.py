import requests
import key

# Your Merriam-Webster API keys
DICTIONARY_API_KEY = key.DICTIONARY_API_KEY
THESAURUS_API_KEY = key.THESAURUS_API_KEY

# Base URLs
DICTIONARY_URL = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"
THESAURUS_URL = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/"

# Function to get word meaning with concise definitions and idiomatic phrases
def get_meaning(word):
    url = f"{DICTIONARY_URL}{word}?key={DICTIONARY_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and isinstance(data[0], dict):
            result = f"\nMeaning of '{word}':\n"
            for definition in data[0].get("shortdef", []):
                result += f" - {definition}\n"
            idiomatic_phrases = data[0].get("def", [{}])[0].get("sseq", [])
            result += "\nIdiomatic Phrases (if any):\n"
            for sseq_item in idiomatic_phrases:
                for item in sseq_item:
                    if "dt" in item[1]:
                        for dt_entry in item[1]["dt"]:
                            if isinstance(dt_entry, list) and "phrase" in dt_entry[0]:
                                result += f" - {dt_entry[1]}\n"
            return result.strip()
        else:
            return f"Sorry, no meaning found for '{word}'."
    else:
        return "Error retrieving data. Please try again."

# Function to get word synonyms and related words
def get_synonyms(word):
    url = f"{THESAURUS_URL}{word}?key={THESAURUS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and isinstance(data[0], dict):
            synonyms = data[0].get("meta", {}).get("syns", [])
            related_words = data[0].get("meta", {}).get("rel_list", [])
            result = ""
            if synonyms:
                result += f"\nSynonyms for '{word}': {', '.join(synonyms[0])}\n"
            else:
                result += f"\nSorry, no synonyms found for '{word}'.\n"
            if related_words:
                result += f"Related Words: {', '.join(related_words[0])}\n"
            else:
                result += "No related words found.\n"
            return result.strip()
        else:
            return f"Sorry, no synonyms or related words found for '{word}'."
    else:
        return "Error retrieving data. Please try again."

# Function to get word antonyms
def get_antonyms(word):
    url = f"{THESAURUS_URL}{word}?key={THESAURUS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and isinstance(data[0], dict):
            antonyms = data[0].get("meta", {}).get("ants", [])
            if antonyms:
                return f"\nAntonyms for '{word}': {', '.join(antonyms[0])}\n"
            else:
                return f"\nSorry, no antonyms found for '{word}'.\n"
        else:
            return f"Sorry, no antonyms found for '{word}'."
    else:
        return "Error retrieving data. Please try again."

# Function to get spelling suggestions
def get_spelling_suggestions(word):
    url = f"{DICTIONARY_URL}{word}?key={DICTIONARY_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and isinstance(data, list) and all(isinstance(item, str) for item in data):
            return f"\nSpelling Suggestions for '{word}': {', '.join(data)}\n"
        else:
            return f"No spelling suggestions found for '{word}'."
    else:
        return "Error retrieving data. Please try again."

# Helper function to handle dictionary features from main code
def handle_dictionary_input(user_input):
    user_input_lower = user_input.lower()
    if "meaning of" in user_input_lower:
        word = user_input_lower.replace("meaning of", "").strip()
        return get_meaning(word)
    elif "synonym of" in user_input_lower:
        word = user_input_lower.replace("synonym of", "").strip()
        return get_synonyms(word)
    elif "antonym of" in user_input_lower:
        word = user_input_lower.replace("antonym of", "").strip()
        return get_antonyms(word)
    elif "spelling of" in user_input_lower:
        word = user_input_lower.replace("spelling of", "").strip()
        return get_spelling_suggestions(word)
    else:
        return "Sorry, I couldn't understand your dictionary request."

