import unittest
import os
from main import read_config, read_csv, create_anki_cards, process_decks

class TestAnkiSprachenLernen(unittest.TestCase):

    def setUp(self):
        # Beispielkonfiguration
        self.config = {
            'audio_path': 'projects/sample_project/data/audio',
            'audio_extension': '.mp3',
            'image_path': 'projects/sample_project/data/images',
            'image_extension': '.jpg',
            'decks': [
                {
                    'name': 'Main Deck',
                    'subdecks': [
                        {
                            'name': 'Subdeck 1',
                            'csv_file': 'projects/sample_project/data/vocab/subdeck1.csv',
                            'csv_headers': ['Deutsch', 'Romaji', 'Hiragana', 'Katakana'],
                            'cards': [
                                {'front': '{Deutsch} - {Romaji} {Bild}', 'back': '{Hiragana} - {Katakana} {Audio}'},
                                {'front': '{Deutsch} {Bild}', 'back': '{Hiragana} ({Romaji}) {Audio}'},
                                {'front': '{Romaji} {Bild}', 'back': '{Deutsch} - {Katakana} {Audio}'}
                            ],
                            'subdecks': [
                                {
                                    'name': 'Subdeck 1.1',
                                    'csv_file': 'projects/sample_project/data/vocab/subdeck1_1.csv',
                                    'csv_headers': ['Deutsch', 'Romaji', 'Hiragana', 'Katakana'],
                                    'cards': [
                                        {'front': '{Deutsch} - {Romaji} {Bild}', 'back': '{Hiragana} - {Katakana} {Audio}'},
                                        {'front': '{Deutsch} {Bild}', 'back': '{Hiragana} ({Romaji}) {Audio}'},
                                        {'front': '{Romaji} {Bild}', 'back': '{Deutsch} - {Katakana} {Audio}'}
                                    ]
                                }
                            ]
                        },
                        {
                            'name': 'Subdeck 2',
                            'csv_file': 'projects/sample_project/data/vocab/subdeck2.csv',
                            'csv_headers': ['Wort', 'Transliteration', 'Hiragana', 'Katakana'],
                            'cards': [
                                {'front': '{Wort} - {Transliteration} {Bild}', 'back': '{Hiragana} - {Katakana} {Audio}'},
                                {'front': '{Wort} {Bild}', 'back': '{Hiragana} ({Transliteration}) {Audio}'},
                                {'front': '{Transliteration} {Bild}', 'back': '{Wort} - {Katakana} {Audio}'}
                            ]
                        }
                    ]
                }
            ]
        }
        # Beispieldaten für Subdeck 1
        self.csv_data_subdeck1 = [
            {'Deutsch': 'Hund', 'Romaji': 'inu', 'Hiragana': 'いぬ', 'Katakana': 'イヌ'},
            {'Deutsch': 'Katze', 'Romaji': 'neko', 'Hiragana': 'ねこ', 'Katakana': 'ネコ'}
        ]
        # Beispieldaten für Subdeck 1.1
        self.csv_data_subdeck1_1 = [
            {'Deutsch': 'Baum', 'Romaji': 'ki', 'Hiragana': 'き', 'Katakana': 'キ'},
            {'Deutsch': 'Blume', 'Romaji': 'hana', 'Hiragana': 'はな', 'Katakana': 'ハナ'}
        ]
        # Beispieldaten für Subdeck 2
        self.csv_data_subdeck2 = [
            {'Wort': 'Berg', 'Transliteration': 'yama', 'Hiragana': 'やま', 'Katakana': 'ヤマ'},
            {'Wort': 'See', 'Transliteration': 'umi', 'Hiragana': 'うみ', 'Katakana': 'ウミ'}
        ]
        # Beispiel Audio- und Bild-Dateien (zum Testen, wir verwenden einen temporären Pfad)
        os.makedirs(self.config['audio_path'], exist_ok=True)
        os.makedirs(self.config['image_path'], exist_ok=True)
        for item in self.csv_data_subdeck1 + self.csv_data_subdeck1_1 + self.csv_data_subdeck2:
            with open(f"{self.config['audio_path']}/{item['Hiragana']}{self.config['audio_extension']}", 'w') as f:
                f.write("dummy audio content")
            with open(f"{self.config['image_path']}/{item['Hiragana']}{self.config['image_extension']}", 'w') as f:
                f.write("dummy image content")

    def tearDown(self):
        # Lösche die temporären Audio- und Bild-Dateien
        for item in self.csv_data_subdeck1 + self.csv_data_subdeck1_1 + self.csv_data_subdeck2:
            os.remove(f"{self.config['audio_path']}/{item['Hiragana']}{self.config['audio_extension']}")
            os.remove(f"{self.config['image_path']}/{item['Hiragana']}{self.config['image_extension']}")
        os.rmdir(self.config['audio_path'])
        os.rmdir(self.config['image_path'])

    def test_read_config(self):
        config = read_config('config.yaml')
        self.assertEqual(config, self.config)

    def test_read_csv(self):
        data_subdeck1 = read_csv('projects/sample_project/data/vocab/subdeck1.csv', self.config['decks'][0]['subdecks'][0]['csv_headers'])
        data_subdeck1_1 = read_csv('projects/sample_project/data/vocab/subdeck1_1.csv', self.config['decks'][0]['subdecks'][0]['subdecks'][0]['csv_headers'])
        data_subdeck2 = read_csv('projects/sample_project/data/vocab/subdeck2.csv', self.config['decks'][0]['subdecks'][1]['csv_headers'])
        self.assertEqual(data_subdeck1, self.csv_data_subdeck1)
        self.assertEqual(data_subdeck1_1, self.csv_data_subdeck1_1)
        self.assertEqual(data_subdeck2, self.csv_data_subdeck2)

    def test_create_anki_cards(self):
        cards_subdeck1 = create_anki_cards(self.csv_data_subdeck1, self.config['decks'][0]['subdecks'][0]['cards'], self.config['audio_path'], self.config['audio_extension'], self.config['image_path'], self.config['image_extension'])
        cards_subdeck1_1 = create_anki_cards(self.csv_data_subdeck1_1, self.config['decks'][0]['subdecks'][0]['subdecks'][0]['cards'], self.config['audio_path'], self.config['audio_extension'], self.config['image_path'], self.config['image_extension'])
        cards_subdeck2 = create_anki_cards(self.csv_data_subdeck2, self.config['decks'][0]['subdecks'][1]['cards'], self.config['audio_path'], self.config['audio_extension'], self.config['image_path'], self.config['image_extension'])
        expected_cards_subdeck1 = [
            {'front': 'Hund - inu <img src=\'projects/sample_project/data/images/いぬ.jpg\'>', 'back': 'いぬ - イヌ [sound:projects/sample_project/data/audio/いぬ.mp3]'},
            {'front': 'Hund <img src=\'projects/sample_project/data/images/いぬ.jpg\'>', 'back': 'いぬ (inu) [sound:projects/sample_project/data/audio/いぬ.mp3]'},
            {'front': 'inu <img src=\'projects/sample_project/data/images/いぬ.jpg\'>', 'back': 'Hund - イヌ [sound:projects/sample_project/data/audio/いぬ.mp3]'},
            {'front': 'Katze - neko <img src=\'projects/sample_project/data/images/ねこ.jpg\'>', 'back': 'ねこ - ネコ [sound:projects/sample_project/data/audio/ねこ.mp3]'},
            {'front': 'Katze <img src=\'projects/sample_project/data/images/ねこ.jpg\'>', 'back': 'ねこ (neko) [sound:projects/sample_project/data/audio/ねこ.mp3]'},
            {'front': 'neko <img src=\'projects/sample_project/data/images/ねこ.jpg\'>', 'back': 'Katze - ネコ [sound:projects/sample_project/data/audio/ねこ.mp3]'}
        ]
        expected_cards_subdeck1_1 = [
            {'front': 'Baum - ki <img src=\'projects/sample_project/data/images/き.jpg\'>', 'back': 'き - キ [sound:projects/sample_project/data/audio/き.mp3]'},
            {'front': 'Baum <img src=\'projects/sample_project/data/images/き.jpg\'>', 'back': 'き (ki) [sound:projects/sample_project/data/audio/き.mp3]'},
            {'front': 'ki <img src=\'projects/sample_project/data/images/き.jpg\'>', 'back': 'Baum - キ [sound:projects/sample_project/data/audio/き.mp3]'},
            {'front': 'Blume - hana <img src=\'projects/sample_project/data/images/はな.jpg\'>', 'back': 'はな - ハナ [sound:projects/sample_project/data/audio/はな.mp3]'},
            {'front': 'Blume <img src=\'projects/sample_project/data/images/はな.jpg\'>', 'back': 'はな (hana) [sound:projects/sample_project/data/audio/はな.mp3]'},
            {'front': 'hana <img src=\'projects/sample_project/data/images/はな.jpg\'>', 'back': 'Blume - ハナ [sound:projects/sample_project/data/audio/はな.mp3]'}
        ]
        expected_cards_subdeck2 = [
            {'front': 'Berg - yama <img src=\'projects/sample_project/data/images/やま.jpg\'>', 'back': 'やま - ヤマ [sound:projects/sample_project/data/audio/やま.mp3]'},
            {'front': 'Berg <img src=\'projects/sample_project/data/images/やま.jpg\'>', 'back': 'やま (yama) [sound:projects/sample_project/data/audio/やま.mp3]'},
            {'front': 'yama <img src=\'projects/sample_project/data/images/やま.jpg\'>', 'back': 'Berg - ヤマ [sound:projects/sample_project/data/audio/やま.mp3]'},
            {'front': 'See - umi <img src=\'projects/sample_project/data/images/うみ.jpg\'>', 'back': 'うみ - ウミ [sound:projects/sample_project/data/audio/うみ.mp3]'},
            {'front': 'See <img src=\'projects/sample_project/data/images/うみ.jpg\'>', 'back': 'うみ (umi) [sound:projects/sample_project/data/audio/うみ.mp3]'},
            {'front': 'umi <img src=\'projects/sample_project/data/images/うみ.jpg\'>', 'back': 'See - ウミ [sound:projects/sample_project/data/audio/うみ.mp3]'}
        ]
        self.assertEqual(cards_subdeck1, expected_cards_subdeck1)
        self.assertEqual(cards_subdeck1_1, expected_cards_subdeck1_1)
        self.assertEqual(cards_subdeck2, expected_cards_subdeck2)

    def test_process_decks(self):
        all_decks = process_decks(self.config['decks'], self.config)
        self.assertEqual(len(all_decks), 3)
        self.assertEqual(all_decks[0]['deck'], 'Main Deck::Subdeck 1')
        self.assertEqual(all_decks[1]['deck'], 'Main Deck::Subdeck 1::Subdeck 1.1')
        self.assertEqual(all_decks[2]['deck'], 'Main Deck::Subdeck 2')

if __name__ == '__main__':
    unittest.main()
