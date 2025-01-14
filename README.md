# Android to Xcode String Catalog Converter 🚀

This script helps you convert your Android `strings.xml` files into an Xcode-compatible `.xcstrings` format (String Catalog). After conversion, you can easily import the generated file into your Xcode project for localization.

## How to Use

### 1. Prepare the Input Files
- Copy all your Android `strings.xml` files into the `inputFolder` directory.
- Name each file according to its locale. For example:
  - The `strings.xml` for German: `de.xml`
  - The `strings.xml` for English: `en.xml`
  
  You can have as many localized files as needed (e.g., `fr.xml`, `es.xml`, etc.).

### 2. Run the Script
Once your files are ready, simply run the script using the following command:

```bash
python3 script.py
```

### 3. Output
After running the script, it will generate a `Localizable.xcstrings` file in the same directory. This file is in the `.xcstrings` format and can be directly imported into your Xcode project for localization.

### 4. Import into Xcode
- Drag and drop the generated `Localizable.xcstrings` file into your Xcode project.
- Start using the string catalog in your code by referring to the keys defined in the `.xcstrings` file.

---

## Requirements

- Python 3.x
- Libraries: `xml.etree.ElementTree` (used for parsing Android XML files, should already be installed)

---

## Notes
- If no `en.xml` (English) file is found, the script will use the first available file as the default language.
- The output `.xcstrings` file will contain all your translations in the required format for Xcode string catalogs.

---

Feel free to open an issue if you encounter any bugs or have questions!
