from deep_translator import GoogleTranslator
import langid
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

# Custom dictionaries to handle specific words/phrases for translation
english_to_hindi_dict = {
    "super breakfast": "supra bhaat",
    "hard work": "parishram",
    "struggle": "sangharsh",
    "success": "safalta",  # Add more words as needed
}

hindi_to_english_dict = {
    "supra bhaat": "super breakfast",
    "parishram": "hard work",
    "sangharsh": "struggle",
    "safalta": "success",  # Add more words as needed
}

def transliterate_text(text, from_lang='en', to_lang='hi'):
    """
    Transliterate Latin text (English/Hindi in Latin script) to Hindi script.
    """
    try:
        # Transliterate from English or transliterated Hindi to Hindi
        if from_lang == 'en' and to_lang == 'hi':
            return transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)
        return text
    except Exception as e:
        print(f"Error during transliteration: {e}")
    return text

def translate_text(text, from_lang='en', to_lang='hi'):
    """
    Translate text from one language to another.
    """
    try:
        # Check if text contains any special words from the dictionary
        for english_word, hindi_translation in english_to_hindi_dict.items():
            if english_word.lower() in text.lower():
                print(f"Word '{english_word}' found. Replacing with '{hindi_translation}'")
                text = text.lower().replace(english_word, hindi_translation)

        # Translate sentence using Google Translator
        translated = GoogleTranslator(source=from_lang, target=to_lang).translate(text)
        print(f"Translated text: {translated}")
        return translated
    except Exception as e:
        print(f"Error during translation: {e}")
    return None

def translate_text_hindi_to_english(text, from_lang='hi', to_lang='en'):
    """
    Translate Hindi text to English.
    """
    try:
        # Check if text contains any special words from the dictionary
        for hindi_word, english_translation in hindi_to_english_dict.items():
            if hindi_word.lower() in text.lower():
                print(f"Word '{hindi_word}' found. Replacing with '{english_translation}'")
                text = text.lower().replace(hindi_word, english_translation)

        # Translate sentence using Google Translator
        translated = GoogleTranslator(source=from_lang, target=to_lang).translate(text)
        print(f"Translated text: {translated}")
        return translated
    except Exception as e:
        print(f"Error during translation: {e}")
    return None

def main():
    print("Text-based Translation System")
    
    # Get input from the user
    user_input = input("Enter a sentence to be translated: ")
    
    # Detect the language of the input text using langid
    detected_lang, _ = langid.classify(user_input)
    print(f"Detected language: {detected_lang}")
    
    # Check if input is in English or Hindi (both script and transliterated)
    if detected_lang == 'en':  # English input
        translated_text_hi = translate_text(user_input, from_lang='en', to_lang='hi')
        if translated_text_hi:
            print(f"Translated to Hindi: {translated_text_hi}")
    elif detected_lang == 'hi' or detected_lang == 'und':  # Hindi input or uncertain language (transliterated)
        # Handle Hindi input directly or transliterated Hindi
        translated_text_en = translate_text_hindi_to_english(user_input, from_lang='hi', to_lang='en')
        if translated_text_en:
            print(f"Translated to English: {translated_text_en}")
    else:
        # If language detection is uncertain, try to transliterate Latin input to Hindi
        print("Detected language is uncertain, checking for transliterated Hindi...")

        # First, try transliterating Latin input to Hindi script
        transliterated_text = transliterate_text(user_input, from_lang='en', to_lang='hi')
        print(f"Transliterated text to Hindi: {transliterated_text}")

        # Now translate the transliterated text to Hindi
        translated_text_hi = translate_text(transliterated_text, from_lang='en', to_lang='hi')
        if translated_text_hi:
            print(f"Translated to Hindi: {translated_text_hi}")


