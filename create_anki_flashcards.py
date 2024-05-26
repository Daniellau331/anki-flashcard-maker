import requests
from lib import download_pronunciations as mp3_download
import os

def invoke(action, params):
    return requests.post('http://localhost:8765', json={'action': action, 'params': params, 'version': 6}).json()

def add_deck(deck_name):
    result = invoke('createDeck', {'deck': deck_name})
    if result.get('error'):
        print(f"Error creating deck: {result['error']}")
    else:
        print(f"Deck '{deck_name}' created successfully.")

def create_word_pronounciation(deck_name, word):
    # download the word's pronounciation 
    mp3_download.download_mp3(word)

    mp3_path = f"./pronunciations/{word}.mp3"

    note_data = {
        "deckName": deck_name,
        "modelName": "Basic",
        "fields": {
            "Front": f"{word} <br> [sound:{os.path.basename(mp3_path)}]" if mp3_path else word,
            "Back": "" 
        },
        "options": {
            "allowDuplicate": False
        }
    } 
    add_flashcard(deck_name,note=note_data)


def add_flashcard(deck_name, front=None, back=None, note=None):
    # Ensure the deck exists
    deck_names = invoke('deckNames', {})
    if deck_name not in deck_names['result']:
        add_deck(deck_name)


    # Define the note (flashcard) to add
    if note:
        note_data = note
    else:
        note_data = {
            "deckName": deck_name,
            "modelName": "Basic",
            "fields": {
                "Front": front,
                "Back": back
            },
            "options": {
                "allowDuplicate": False
            }
        }

    # Send the request to AnkiConnect
    response = requests.post(
        "http://localhost:8765",
        json={"action": "addNote", "version": 6, "params": {"note": note}}
    )

    # Check the response
    if response.status_code == 200:
        result = response.json()
        if result.get("error") is None:
            print("Flashcard added successfully!")
        else:
            print("Error:", result["error"])
    else:
        print("Error:", response.text)

# Example usage
create_word_pronounciation("My Deck", "old")
# add_flashcard("My Deck", "What is the capital of France?", "Paris")
