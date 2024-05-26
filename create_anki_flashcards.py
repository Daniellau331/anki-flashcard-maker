import requests
from lib import download_pronunciations as mp3_download

def invoke(action, params):
    return requests.post('http://localhost:8765', json={'action': action, 'params': params, 'version': 6}).json()

def add_deck(deck_name):
    result = invoke('createDeck', {'deck': deck_name})
    if result.get('error'):
        print(f"Error creating deck: {result['error']}")
    else:
        print(f"Deck '{deck_name}' created successfully.")

def add_flashcard(deck_name, front, back):
    # Ensure the deck exists
    deck_names = invoke('deckNames', {})
    if deck_name not in deck_names['result']:
        add_deck(deck_name)

    # test the mp3 code
    mp3_download.download_mp3("coffee")

    # Define the note (flashcard) to add
    note = {
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
add_flashcard("My Deck", "What is the capital of France?", "Paris")
