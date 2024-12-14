# Dictionary Anki Deck Generator

This script generates an Anki deck from a list of words by fetching detailed dictionary data (including phonetics, audio, meanings, synonyms, and antonyms) using the [DictionaryAPI](https://dictionaryapi.dev). The generated deck is styled and designed for effective vocabulary learning.

## Features
- **Custom Anki Cards**: Each card includes:
  - Word
  - Phonetics
  - Audio pronunciation
  - Meanings (with examples where available)
  - Synonyms and antonyms
- **Progress Bar**: Displays real-time progress in the console during deck creation.
- **Media Support**: Automatically downloads audio pronunciation files and includes them in the Anki deck.
- **HTML Styling**: Cards have an elegant design for better readability.

## Requirements

### Python Libraries
- `requests`: For fetching word data from the DictionaryAPI.
- `genanki`: For creating and exporting Anki decks.
- `urllib`: For downloading audio files.

Install these libraries using pip:

```bash
pip install requests genanki
