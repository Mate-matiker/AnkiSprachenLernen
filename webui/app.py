from flask import Flask, render_template, request, redirect, url_for
import yaml
import traceback

app = Flask(__name__)

def parse_subdecks(request, prefix, subdeck_count):
    subdecks = []
    for i in range(subdeck_count):
        subdeck_name = request.form.get(f'{prefix}_subdeck_name_{i}')
        subdeck_csv = request.form.get(f'{prefix}_subdeck_csv_{i}')
        csv_headers = request.form.get(f'{prefix}_csv_headers_{i}').split(',')
        card_count = int(request.form.get(f'{prefix}_card_count_{i}'))

        cards = []
        for j in range(card_count):
            front = request.form.get(f'{prefix}_card_{i}_front_{j}')
            back = request.form.get(f'{prefix}_card_{i}_back_{j}')
            cards.append({'front': front, 'back': back})

        subdeck_subdeck_count_str = request.form.get(f'{prefix}_subdeck_{i}_subdeck_count')
        if subdeck_subdeck_count_str is None:
            subdeck_subdeck_count = 0
        else:
            subdeck_subdeck_count = int(subdeck_subdeck_count_str)

        subdeck_subdecks = parse_subdecks(request, f'{prefix}_subdeck_{i}', subdeck_subdeck_count)

        subdecks.append({
            'name': subdeck_name,
            'csv_file': subdeck_csv,
            'csv_headers': csv_headers,
            'cards': cards,
            'subdecks': subdeck_subdecks
        })
    return subdecks

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_config', methods=['POST'])
def generate_config():
    try:
        main_deck_name = request.form.get('main_deck_name')
        audio_path = request.form.get('audio_path')
        audio_extension = request.form.get('audio_extension')
        image_path = request.form.get('image_path')
        image_extension = request.form.get('image_extension')

        subdeck_count_str = request.form.get('subdeck_count')
        if subdeck_count_str is None:
            subdeck_count = 0
        else:
            subdeck_count = int(subdeck_count_str)

        subdecks = parse_subdecks(request, 'main', subdeck_count)

        config_data = {
            'decks': [
                {
                    'name': main_deck_name,
                    'subdecks': subdecks,
                },
            ],
            'audio_path': audio_path,
            'audio_extension': audio_extension,
            'image_path': image_path,
            'image_extension': image_extension,
        }

        with open('config.yaml', 'w') as file:
            yaml.dump(config_data, file)

        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print(traceback.format_exc())
        return "An error occurred while generating the config file. Check the server logs for more details.", 500

if __name__ == '__main__':
    app.run(debug=True)
