import csv
import yaml
import os

# Funktion zum Einlesen der Konfigurationsdatei
def read_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Funktion zum Einlesen der CSV-Datei
def read_csv(csv_file, headers):
    with open(csv_file, 'r', encoding='utf-8') as file):
        reader = csv.DictReader(file, fieldnames=headers)
    next(reader)  # Skip header row
    return [row for row in reader]

# Funktion zum Erstellen der Anki-Karten basierend auf der Konfiguration
def create_anki_cards(data, card_templates, audio_path, audio_extension, image_path, image_extension):
    cards = []
    for item in data:
        # Generiere den Audio-Dateipfad
        audio_file = f"{audio_path}/{item['Hiragana']}{audio_extension}"
        audio_tag = f"[sound:{audio_file}]" if os.path.exists(audio_file) else ""

        # Generiere den Bild-Dateipfad
        image_file = f"{image_path}/{item['Hiragana']}{image_extension}"
        image_tag = f"<img src='{image_file}'>" if os.path.exists(image_file) else ""

        # Füge die Media-Tags zu den Daten hinzu
        item['Audio'] = audio_tag
        item['Bild'] = image_tag

        for template in card_templates:
            front = template['front'].format(**item)
            back = template['back'].format(**item)
            cards.append({'front': front, 'back': back})
    return cards

# Rekursive Funktion zum Verarbeiten der Decks und Subdecks
def process_decks(decks, global_config, parent_deck_name=""):
    all_cards = []
    for deck in decks:
        current_deck_name = f"{parent_deck_name}::{deck['name']}" if parent_deck_name else deck['name']

        # Verarbeiten der CSV-Datei, wenn vorhanden
        if 'csv_file' in deck:
            csv_data = read_csv(deck['csv_file'], deck['csv_headers'])
            anki_cards = create_anki_cards(csv_data, deck['cards'], global_config['audio_path'], global_config['audio_extension'], global_config['image_path'], global_config['image_extension'])
            all_cards.append({'deck': current_deck_name, 'cards': anki_cards})

        # Rekursiv die Subdecks verarbeiten, wenn vorhanden
        if 'subdecks' in deck:
            subdeck_cards = process_decks(deck['subdecks'], global_config, current_deck_name)
            all_cards.extend(subdeck_cards)

    return all_cards

# Hauptfunktion
def main():
    # Einlesen der Konfiguration
    config = read_config('config.yaml')

    # Verarbeiten der Decks und Subdecks
    all_decks = process_decks(config['decks'], config)

    # Ausgabe der Anki-Karten (kann später durch Export in Anki-Format ersetzt werden)
    for deck in all_decks:
        print(f"Deck: {deck['deck']}")
        for card in deck['cards']:
            print(f"  Front: {card['front']}")
            print(f"  Back: {card['back']}\n")

if __name__ == "__main__":
    main()
