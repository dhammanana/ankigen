import os
import requests
import genanki
import urllib.request
import hashlib
import random
import sys
import time

def print_progress(current, total, prefix="Progress", bar_length=40):
    """
    Prints a progress bar to the console.
    
    :param current: The current progress value (e.g., iteration count).
    :param total: The total value for completion.
    :param prefix: A prefix string to display before the progress bar.
    :param bar_length: The length of the progress bar (number of characters).
    """
    # Calculate the percentage of completion
    progress = current / total
    block = int(round(bar_length * progress))
    
    # Create the progress bar string
    bar = f"[{'#' * block}{'-' * (bar_length - block)}]"
    percent = f"{progress * 100:.2f}%"
    
    # Print the progress bar
    sys.stdout.write(f"\r{prefix}: {bar} {percent} ({current}/{total})")
    sys.stdout.flush()

    # Print a newline when finished
    if current == total:
        print()  # Move to the next line

class DictionaryAnkiGenerator:
    def __init__(self, word_list, deck_name="Dictionary Vocabulary"):
        """
        Initialize the Anki deck generator
        
        :param word_list: List of words to create Anki cards for
        :param deck_name: Name of the Anki deck
        """
        self.word_list = word_list
        self.deck_name = deck_name
        self.model = self._create_model()
        self.deck = genanki.Deck(random.randrange(1 << 30, 1 << 31), deck_name)
        self.package = genanki.Package(self.deck)

    def _create_model(self):
        """
        Create a custom Anki card model with multiple fields and improved styling
        """
        return genanki.Model(
            random.randrange(1 << 30, 1 << 31),
            'Dictionary Card',
            fields=[
                {'name': 'Word'},
                {'name': 'Phonetics'},
                {'name': 'AudioFilename'},
                {'name': 'Meanings'},
                {'name': 'Synonyms'},
                {'name': 'Antonyms'}
            ],
            templates=[
                {
                    'name': 'Card',
                    'qfmt': '''
                    <div style="
                        background-color: #000408; 
                        border-radius: 15px; 
                        padding: 20px; 
                        text-align: center; 
                        font-family: Arial, sans-serif;
                    ">
                        <h1 style="
                            color:white;
                            font-size: 36px; 
                            margin-bottom: 10px; 
                            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
                        ">{{Word}}</h1>
                        <div style="
                            color: #7f8c8d; 
                            font-size: 18px; 
                            margin-bottom: 15px;
                        ">{{Phonetics}}</div>
                    </div>
                    ''',
                    'afmt': '''
                    <div style="
                        background-color: #000408; 
                        border-radius: 15px; 
                        padding: 20px; 
                        font-family: Arial, sans-serif;
                    ">
                        <h1 style="
                            color: white; 
                            font-size: 36px; 
                            margin-bottom: 10px; 
                            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
                        ">{{Word}}</h1>
                        
                        <div style="
                            color: #7f8c8d; 
                            font-size: 18px; 
                            margin-bottom: 15px;
                        ">{{Phonetics}}</div>
                        
                        {{#AudioFilename}}
                            {{AudioFilename}}
                        {{/AudioFilename}}

                        <div style="
                            background-color: #333; 
                            border-radius: 10px; 
                            padding: 15px; 
                            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                        ">
                            <h2 style="
                                color: #3498db; 
                                border-bottom: 2px solid #3498db; 
                                padding-bottom: 10px; 
                                margin-bottom: 15px;
                            ">Meanings</h2>
                            {{Meanings}}
                        </div>
                        
                        <div style="
                            margin-top: 15px; 
                            display: flex; 
                            justify-content: space-between;
                        ">
                            <div style="
                                background-color: #303; 
                                border-radius: 10px; 
                                padding: 10px; 
                                width: 48%;
                            ">
                                <h3 style="
                                    color: #2980b9; 
                                    margin-bottom: 10px;
                                ">Synonyms</h3>
                                {{Synonyms}}
                            </div>
                            
                            <div style="
                                background-color: #330; 
                                border-radius: 10px; 
                                padding: 10px; 
                                width: 48%;
                            ">
                                <h3 style="
                                    color: #c0392b; 
                                    margin-bottom: 10px;
                                ">Antonyms</h3>
                                {{Antonyms}}
                            </div>
                        </div>
                    </div>
                    '''
                }
            ]
        )

    def _download_audio(self, audio_url, word):
        """
        Download audio file for a word and add to Anki package
        
        :param audio_url: URL of the audio file
        :param word: Word for which audio is being downloaded
        :return: Filename of the audio file or empty string
        """
        if not audio_url:
            return ''
        
        try:
            # Generate a consistent filename
            audio_filename = f'audio/audio_{word}.mp3'
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(audio_url, audio_filename)
            
            # Add the file to the Anki package
            self.package.media_files.append(audio_filename)
            
            return audio_filename.split('/')[-1]
        except Exception as e:
            print(f"Could not download audio for {word}: {e}")
            return ''

    def _get_word_info(self, word):
        """
        Fetch dictionary information for a word
        
        :param word: Word to look up
        :return: Dictionary with word information
        """
        try:
            response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
            response.raise_for_status()
            return response.json()[0]
        except Exception as e:
            print(f"Error fetching dictionary info for {word}: {e}")
            return None

    def generate_deck(self, output_filename=None):
        """
        Generate Anki deck from the word list
        
        :param output_filename: Optional filename for the Anki package
        """
        for i in range(len(self.word_list)):
            word = self.word_list[i]
            print_progress(i + 1, len(self.word_list), prefix="Progress", bar_length=40)
            word_info = self._get_word_info(word)
            if not word_info:
                continue

            # Extract phonetics

            phonetics_list = word_info.get('phonetics', [])
            if phonetics_list:
                phonetics = phonetics_list[0].get('text', 'N/A')
            else:
                phonetics = 'N/A'
            
            # Find audio URL and download
            audio_url = next((p.get('audio') for p in word_info.get('phonetics', []) if p.get('audio')), '')
            audio_filename = self._download_audio(audio_url, word)

            # Process meanings with improved HTML
            meanings_html = ''
            for meaning in word_info.get('meanings', []):
                part_of_speech = meaning.get('partOfSpeech', '')
                definitions = meaning.get('definitions', [])
                
                for def_item in definitions:
                    definition = def_item.get('definition', '')
                    example = def_item.get('example', '')
                    
                    meanings_html += f'''
                    <div style="
                        margin-bottom: 15px; 
                        padding: 10px; 
                        background-color: #010304; 
                        border-radius: 5px;
                    ">
                        <p style="
                            color: yellow; 
                            font-weight: bold; 
                            margin-bottom: 5px;
                        ">{part_of_speech.capitalize()}</p>
                        <p style="margin-bottom: 5px;">{definition}</p>
                        {f'<p style="color: #7f8c8d; font-style: italic;">Example: {example}</p>' if example else ''}
                    </div>
                    '''

                # Find synonyms and antonyms (if available)
                synonyms = ', '.join(meaning.get('synonyms', [])) or 'N/A'
                antonyms = ', '.join(meaning.get('antonyms', [])) or 'N/A'

            # Create Anki note
            note = genanki.Note(
                model=self.model,
                fields=[
                    word,
                    phonetics,
                    f"[sound:{audio_filename}]",
                    meanings_html,
                    synonyms,
                    antonyms
                ]
            )
            
            # Add note to deck
            self.deck.add_note(note)

        # Generate Anki package
        output_filename = output_filename or f'{self.deck_name}.apkg'
        self.package.write_to_file(output_filename)
        print(f"Anki deck generated: {output_filename}")

# Example usage
if __name__ == "__main__":
    # List of words to create Anki cards for
    words = ['abolish', 'serendipity', 'eloquent']
    with open('words.txt') as f:
        for line in f.readlines():
            word = line.split(' ')[0]
            words.append(word)
    
    
    # Create and generate Anki deck
    anki_generator = DictionaryAnkiGenerator(words)
    anki_generator.generate_deck()