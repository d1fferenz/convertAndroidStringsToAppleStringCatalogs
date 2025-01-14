import os
import glob
import json
import xml.etree.ElementTree as ET

# Function to parse Android strings.xml files
def parse_android_strings(file_path):
    strings_dict = {}
    tree = ET.parse(file_path)
    root = tree.getroot()
    for string in root.findall("string"):
        key = string.get("name")
        value = string.text.strip() if string.text else ""
        strings_dict[key] = value
    return strings_dict

# Function to create .xcstrings (JSON) with the required keys
def create_xcstrings(base_lang, other_langs, output_file, base_locale="en"):
    # Prepare the structure for the .xcstrings JSON
    xcstrings_data = {
        "version": "1.0",  # Required version key
        "sourceLanguage": base_locale,  # Required sourceLanguage key
        "strings": {}
    }

    # Iterate through the keys in the base language and populate the structure
    for key, base_value in base_lang.items():
        xcstrings_data["strings"][key] = {
            "extractionState": "automated",
            "localizations": {
                base_locale: {
                    "stringUnit": {
                        "state": "translated",
                        "value": base_value
                    }
                }
            }
        }

        # Add translations for other languages
        for lang, lang_dict in other_langs.items():
            lang_value = lang_dict.get(key, base_value)  # Use base value if translation is missing
            xcstrings_data["strings"][key]["localizations"][lang] = {
                "stringUnit": {
                    "state": "translated",
                    "value": lang_value
                }
            }

    # Write the JSON data to the output file
    with open(output_file, 'w', encoding='utf-8') as output:
        json.dump(xcstrings_data, output, ensure_ascii=False, indent=2)

# Main function to orchestrate the process
def main(input_folder, output_file):
    # Step 1: Find all .xml files in the folder
    xml_files = glob.glob(os.path.join(input_folder, "*.xml"))
    if not xml_files:
        print("Error: No .xml files found in the input folder.")
        return

    # Step 2: Determine the base language (default to "en.xml" if available)
    base_lang_file = None
    languages = {}
    for xml_file in xml_files:
        lang_code = os.path.splitext(os.path.basename(xml_file))[0]  # Get the locale prefix (e.g., "en", "de")
        languages[lang_code] = xml_file
        if lang_code == "en":
            base_lang_file = xml_file

    # Use the first available file as the base language if no "en.xml" exists
    if not base_lang_file:
        base_lang_file = next(iter(languages.values()))
        base_locale = os.path.splitext(os.path.basename(base_lang_file))[0]
        print(f"No 'en.xml' found. Using '{base_lang_file}' as the base language.")
    else:
        base_locale = "en"

    # Step 3: Parse the base language
    base_lang = parse_android_strings(base_lang_file)

    # Step 4: Parse other languages
    other_langs = {}
    for lang_code, xml_file in languages.items():
        if xml_file != base_lang_file:  # Skip the base language
            other_langs[lang_code] = parse_android_strings(xml_file)

    # Step 5: Generate the .xcstrings JSON file
    create_xcstrings(base_lang, other_langs, output_file, base_locale)
    print(f"Successfully created {output_file}")

# Run the script
if __name__ == "__main__":
    input_folder = "./inputFolder"  # Default folder containing the .xml files
    output_file = "Localizable.xcstrings"  # Default output .xcstrings file
    main(input_folder, output_file)

