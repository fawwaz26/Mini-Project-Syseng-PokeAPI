from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from requests.exceptions import RequestException
import logging

app = Flask(__name__)
CORS(app)  # Enables CORS for all domains on all routes

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

@app.route('/api/pokemon/<name>', methods=['GET'])
def get_pokemon(name):
    try:
        response = requests.get(f"{BASE_URL}{name.lower()}", timeout=10)  # Menambahkan timeout
        if response.ok:
            pokemon_data = response.json()
            formatted_data = {
                'id': str(pokemon_data['id']).zfill(4),  # Zero pad the id to 4 digits
                'name': pokemon_data['name'].capitalize(),
                'types': [t['type']['name'].capitalize() for t in pokemon_data['types']],
                'image': pokemon_data['sprites']['other']['official-artwork']['front_default']
            }
            return jsonify(formatted_data)
        else:
            return jsonify({'error': 'Pokemon not found'}), 404
    except RequestException as e:
        logging.error(f"Error fetching data from PokeAPI: {e}")
        return jsonify({'error': 'Failed to fetch data from PokeAPI'}), 500

if __name__ == '__main__':
    # Mengatur konfigurasi untuk deployment
    app.run(debug=False, host='0.0.0.0', port=5000)