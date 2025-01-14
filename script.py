import os
import glob
import json
import xml.etree.ElementTree as ET

def parse_android_strings(file_path):
    strings_dict = {}
    tree = ET.parse(file_path)
    root = tree.getroot()
    for string in root.findall("string"):
        key = string.get("name")
        value = string.text.strip() if string.text else ""
        strings_dict[key] = value
    return strings_dict

def create_xcstrings(base_lang, other_langs, output_file, base_locale="en"):
    xcstrings_data = {
        "version": "1.0",
        "sourceLanguage": base_locale,
        "strings": {}
    }

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

        for lang, lang_dict in other_langs.items():
            lang_value = lang_dict.get(key, base_value) 
            xcstrings_data["strings"][key]["localizations"][lang] = {
                "stringUnit": {
                    "state": "translated",
                    "value": lang_value
                }
            }

    with open(output_file, 'w', encoding='utf-8') as output:
        json.dump(xcstrings_data, output, ensure_ascii=False, indent=2)

def main(input_folder, output_file):
    xml_files = glob.glob(os.path.join(input_folder, "*.xml"))
    if not xml_files:
        print("Error: No .xml files found in the input folder.")
        return

    base_lang_file = None
    languages = {}
    for xml_file in xml_files:
        lang_code = os.path.splitext(os.path.basename(xml_file))[0]
        languages[lang_code] = xml_file
        if lang_code == "en":
            base_lang_file = xml_file

    if not base_lang_file:
        base_lang_file = next(iter(languages.values()))
        base_locale = os.path.splitext(os.path.basename(base_lang_file))[0]
        print(f"No 'en.xml' found. Using '{base_lang_file}' as the base language.")
    else:
        base_locale = "en"

    base_lang = parse_android_strings(base_lang_file)

    other_langs = {}
    for lang_code, xml_file in languages.items():
        if xml_file != base_lang_file:
            other_langs[lang_code] = parse_android_strings(xml_file)


    create_xcstrings(base_lang, other_langs, output_file, base_locale)
    print(f"Successfully created {output_file}")

if __name__ == "__main__":
    input_folder = "./inputFolder"
    output_file = "Localizable.xcstrings"
    main(input_folder, output_file)

