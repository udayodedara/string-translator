import json
import time
from googletrans import Translator
import os

# Initialize the translator
translator = Translator()

def translate_strings(data, source_lang="hi", target_lang="fr", retries=2, delay=1, failed_log=None):
    if isinstance(data, dict):
        return {key: translate_strings(value, source_lang, target_lang, retries, delay, failed_log) for key, value in data.items()}
    elif isinstance(data, list):
        return [translate_strings(item, source_lang, target_lang, retries, delay, failed_log) for item in data]
    elif isinstance(data, str):
        attempt = 0
        while attempt < retries:
            try:
                translated = translator.translate(data, src=source_lang, dest=target_lang).text
                return translated
            except Exception as e:
                print(f"Error translating: '{data}' -> {e}")
                attempt += 1
                if attempt < retries:
                    print(f"Retrying... Attempt {attempt}/{retries}")
                    time.sleep(delay)
                else:
                    failed_log.append(data)
                    return data  # Return the original text if translation fails
    else:
        return data
    
# Define the relative output folder and file name
output_folder = "output"  # Folder within the current directory
os.makedirs(output_folder, exist_ok=True)  # Ensure folder exists




# Prompt for input and output file paths
input_file_path = input("Enter the path to the input JSON file: ").strip()
failed_log_path = "failed_translations.json"

# Allow dynamic input for the target language
target_lang = input("Enter the target language code (e.g., 'fr' for French): ").strip()

# Save the file with a relative path
output_file_path = os.path.join(output_folder, f"{target_lang}.json")

# Log failed translations
failed_translations = []

# Load the JSON file
try:
    with open(input_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError:
    print("Error: Input file not found. Please check the file path and try again.")
    exit()

# Translate the data
print("Translating data...")
translated_data = translate_strings(data, target_lang=target_lang, failed_log=failed_translations)

# Save the translated data
with open(output_file_path, "w", encoding="utf-8") as output_file:
    json.dump(translated_data, output_file, ensure_ascii=False, indent=4)
    print(f"Translation complete. File saved to {output_file_path}")

# Save failed translations for debugging
if failed_translations:
    with open(failed_log_path, "w", encoding="utf-8") as failed_file:
        json.dump(failed_translations, failed_file, ensure_ascii=False, indent=4)
    print(f"Some translations failed. Check '{failed_log_path}' for details.")
