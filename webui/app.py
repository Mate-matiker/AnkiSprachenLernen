from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import yaml
import os
import traceback

app = Flask(__name__)

CONFIG_DIRECTORY = 'configs'

def parse_subdecks(request, prefix, subdeck_count):
    subdecks = []
    for i in range(subdeck_count):
        subdeck_name = request.form.get(f'{prefix}_subdeck_name_{i}')
        subdeck_csv = request.form.get(f'{prefix}_subdeck_csv_{i}')
        csv_headers = request.form.get(f'{prefix}_csv_headers_{i}').split(',')

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
            'subdecks': subdeck_subdecks
        })
    return subdecks

@app.route('/')
def index():
    config_files = [f for f in os.listdir(CONFIG_DIRECTORY) if f.endswith('.yaml')]
    return render_template('index.html', config_files=config_files)

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

        if not os.path.exists(CONFIG_DIRECTORY):
            os.makedirs(CONFIG_DIRECTORY)

        config_filename = os.path.join(CONFIG_DIRECTORY, f"{main_deck_name.replace(' ', '_')}.yaml")
        with open(config_filename, 'w') as file:
            yaml.dump(config_data, file)

        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print(traceback.format_exc())
        return "An error occurred while generating the config file. Check the server logs for more details.", 500

@app.route('/decks/<filename>')
def get_deck(filename):
    try:
        config_path = os.path.join(CONFIG_DIRECTORY, filename)
        with open(config_path, 'r') as file:
            config_data = yaml.safe_load(file)
        return jsonify(config_data)
    except Exception as e:
        print(f"Error occurred while loading the config file: {str(e)}")
        print(traceback.format_exc())
        return "An error occurred while loading the config file. Check the server logs for more details.", 500

if __name__ == '__main__':
    app.run(debug=True)

