Dictionary Anki Deck Generator

This script generates an Anki deck from a list of words by fetching detailed dictionary data (including phonetics, audio, meanings, synonyms, and antonyms) using the DictionaryAPI. The generated deck is styled and designed for effective vocabulary learning.

Features

Custom Anki Cards: Each card contains fields for:

Word

Phonetics

Audio pronunciation

Meanings (with examples where available)

Synonyms and antonyms


Progress Bar: A console progress bar provides real-time feedback during deck creation.

Media Support: Automatically downloads audio pronunciation files for words and includes them in the Anki deck.

HTML Styling: Cards have a visually appealing design with sections for meanings, examples, synonyms, and antonyms.


Requirements

Python Libraries

requests: For fetching data from the DictionaryAPI.

genanki: For creating and packaging Anki decks.

urllib: For downloading audio files.


Install these libraries using pip:

pip install requests genanki

Other Requirements

An internet connection is required to fetch word definitions and audio.


Usage

1. Prepare a Word List:

Create a file words.txt with one word per line.



2. Run the Script:

Execute the script in a terminal:

python dictionary_anki_generator.py



3. Generated Deck:

The output will be an Anki package file (Dictionary Vocabulary.apkg) in the same directory as the script. You can import this file into Anki.




Code Overview

Main Components

DictionaryAnkiGenerator: The core class responsible for fetching word data, generating notes, and creating the Anki deck.

__init__: Initializes the deck and model.

_create_model: Defines the card template and styling.

_download_audio: Downloads and attaches audio files.

_get_word_info: Fetches word details from the DictionaryAPI.

generate_deck: Generates and saves the Anki package.


print_progress: Displays a progress bar in the console.


Example Workflow

1. The script reads a list of words from words.txt.


2. For each word:

Fetches data from DictionaryAPI (phonetics, meanings, synonyms, antonyms, and audio).

Creates a custom Anki note and adds it to the deck.



3. Finally, the Anki deck is packaged and saved as Dictionary Vocabulary.apkg.



Example Word List (words.txt)

abolish
serendipity
eloquent

Customization

Deck Name: Change the deck_name parameter in the DictionaryAnkiGenerator class to use a custom name.

Card Design: Modify the HTML templates in the _create_model method to change the card layout or styling.


Limitations

The script relies on the DictionaryAPI, which might have limited coverage for some words.

Audio files are fetched from the API and may not be available for all words.


License

This script is open-source and free to use.

