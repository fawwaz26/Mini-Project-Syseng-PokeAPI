from flask import Flask, request, jsonify, render_template, redirect, url_for
from dotenv import load_dotenv
from flask_cors import CORS
import requests
import pymysql
import os
import mysql.connector
from config import DB_CONFIG
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

connector = Connector()

# Fungsi untuk koneksi ke database Google Cloud SQL
def connect_to_database() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "the-dominion-417115:asia-southeast2:pokedexapp",
        "pymysql",
        user="pokedexapp",
        password="fawwazsadri",
        db="pokedexdb"
    )
    return conn

# # Fungsi untuk koneksi ke local database
# def connect_to_database():
#     try:
#         connection = mysql.connector.connect(**DB_CONFIG)
#         return connection
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#         return None

def save_pokemon_detail_to_database(pokemon_detail):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Mengambil URL gambar dari pokemon_detail jika tersedia
            image = pokemon_detail.get('sprites', {}).get('front_default')
            
            cursor.execute("""
                INSERT INTO pokemon_details (id, name, image, hp, attack, defense, description) 
                VALUES (%s, %s, %s, %s, %s, %s, %s) 
                ON DUPLICATE KEY UPDATE 
                name = VALUES(name), image = VALUES(image), hp = VALUES(hp), 
                attack = VALUES(attack), defense = VALUES(defense), description = VALUES(description)
            """,
            (pokemon_detail['id'], pokemon_detail['name'], image, 
             pokemon_detail['stats'][0]['base_stat'], pokemon_detail['stats'][1]['base_stat'], 
             pokemon_detail['stats'][2]['base_stat'], pokemon_detail['description']))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        
        except mysql.connector.Error as err:
            print(f"Error saving Pokémon detail to database: {err}")
            return False


# Fungsi untuk menyimpan ulasan Pokemon ke database
def save_review_to_database(pokemon_name, rating, comment, user_ip, user_agent):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pokemon_reviews (pokemon_name, rating, comment, user_ip, user_agent) VALUES (%s, %s, %s, %s, %s)",
                            (pokemon_name, rating, comment, user_ip, user_agent))
            conn.commit()  # Menyimpan perubahan pada database
            cursor.close()
            conn.close()
            return True
        
        except pymysql.Error as err:
            print(f"Error saving Pokémon review to database: {err}")
            return False

def load_pokemon_detail_from_database(pokemon_id):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pokemon_details WHERE id = %s", (pokemon_id,))
            pokemon_detail = cursor.fetchone()  # Menggunakan fetchone() untuk mengembalikan satu baris dalam bentuk kamus
            cursor.close()
            conn.close()
            return pokemon_detail
        except pymysql.Error as err:
            print(f"Error loading Pokémon detail from database: {err}")
            return None

# Fungsi untuk memuat ulasan Pokemon dari database ke dalam variabel pokemon_reviews
def load_reviews_from_database(pokemon_name):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pokemon_reviews WHERE pokemon_name = %s", (pokemon_name,))
            columns = [col[0] for col in cursor.description]
            reviews = [dict(zip(columns, row)) for row in cursor.fetchall()]
            cursor.close()
            conn.close()
            return reviews
        except mysql.connector.Error as err:
            print(f"Error loading reviews from database: {err}")
            return None


# Fungsi untuk mendapatkan data Pokemon berdasarkan nama
def get_pokemon_by_name(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Fungsi untuk mendapatkan data Pokemon berdasarkan id
def get_pokemon_by_id(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Fungsi untuk mendapatkan deskripsi Pokemon berdasarkan ID karakteristik
def get_pokemon_description(characteristic_id):
    url = f"https://pokeapi.co/api/v2/characteristic/{characteristic_id}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        characteristic_data = response.json()
        description = characteristic_data['descriptions'][7]['description']
        return description
    else:
        return None

# Fungsi untuk mendapatkan semua jenis Pokemon dan URL
def get_all_pokemon_all_type():
    url = "https://pokeapi.co/api/v2/type?limit=-1"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data["results"]
    else:
        return None

# Fungsi untuk mendapatkan ID karakteristik Pokemon berdasarkan nama
def get_characteristic_id(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        pokemon_data = response.json()
        characteristic_id = pokemon_data['id']
        return characteristic_id
    else:
        return 0
    
def get_top_list_pokemon():
    url = "https://pokeapi.co/api/v2/pokemon?limit=20"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        pokemon_list = []

        for pokemon_data in data["results"]:
            pokemon_id = int(pokemon_data["url"].split("/")[-2])
            pokemon_info = get_pokemon_by_id(pokemon_id)
            if pokemon_info:
                pokemon_list.append({
                    "id": pokemon_id,
                    "name": pokemon_info["name"],
                    "image": pokemon_info["sprites"]["front_default"],
                    "hp": pokemon_info["stats"][0]["base_stat"],
                    "attack": pokemon_info["stats"][1]["base_stat"],
                    "defense": pokemon_info["stats"][2]["base_stat"]
                })

        return pokemon_list
    else:
        return None
    
# Mendapatkan daftar Pokemon berdasarkan tipe
def get_list_pokemon(type_name):
    url = f"https://pokeapi.co/api/v2/type/{type_name.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        type_data = response.json()
        pokemon_urls = [p["pokemon"]["url"] for p in type_data["pokemon"]]
        pokemon_list = []

        for url in pokemon_urls:
            pokemon_response = requests.get(url)
            pokemon_data = pokemon_response.json()
            pokemon_list.append({
                "id": pokemon_data["id"],
                "name": pokemon_data["name"],
                "image": pokemon_data["sprites"]["front_default"],
                "image2": pokemon_data["sprites"]["back_default"],
                "hp": pokemon_data["stats"][0]["base_stat"],
                "attack": pokemon_data["stats"][1]["base_stat"],
                "defense": pokemon_data["stats"][2]["base_stat"]
            })

        return pokemon_list
    else:
        return None

# Menyimpan rating dan komentar Pokemon
pokemon_reviews = []

# Menampilkan halaman utama
@app.route('/')
def dashboard():
    all_type = get_all_pokemon_all_type()
    featured_pokemon = get_top_list_pokemon()[:20]
    return render_template('index.html', all_type=all_type, featured_pokemon=featured_pokemon)


# Menampilkan hasil pencarian Pokemon dan detail Pokemon
@app.route('/pokemon', methods=['GET', 'POST'])
@app.route('/pokemon/<pokemon_name>', methods=['GET', 'POST'])
def pokemon(pokemon_name=None):
    global pokemon_reviews
    if request.method == 'POST':
        query = request.form.get('pokemon_name')
        if not query:
            return "Please enter a Pokémon name."

        result = get_pokemon_by_name(query)
        if result:
            characteristic_id = get_characteristic_id(result['name'])
            description = get_pokemon_description(characteristic_id)
            result['description'] = description

            # Save Pokémon detail to database
            if save_pokemon_detail_to_database(result):
                # Load reviews for this Pokémon from the database
                pokemon_reviews = load_reviews_from_database(query)
                return render_template('pokemon.html', pokemon=result, pokemon_reviews=pokemon_reviews)
            else:
                return "Failed to save Pokémon detail to database."
        else:
            return "Invalid Pokémon name."

    if pokemon_name:
        # Check if Pokémon detail already exists in database
        pokemon_detail = load_pokemon_detail_from_database(pokemon_name)
        if not pokemon_detail:
            # Fetch Pokémon detail from API
            pokemon_detail = get_pokemon_by_name(pokemon_name)
            if pokemon_detail:
                characteristic_id = get_characteristic_id(pokemon_detail['name'])
                description = get_pokemon_description(characteristic_id)
                pokemon_detail['description'] = description
                
                # Save Pokémon detail to database
                if not save_pokemon_detail_to_database(pokemon_detail):
                    return "Failed to save Pokémon detail to database."
            
            else:
                return "Pokémon not found."

        # Load reviews for this Pokémon from the database
        pokemon_reviews = load_reviews_from_database(pokemon_name)
        return render_template('pokemon.html', pokemon=pokemon_detail, pokemon_reviews=pokemon_reviews)

    return render_template('pokemon.html', all_type=get_all_pokemon_all_type())


@app.route('/rate', methods=['POST'])
def rate_pokemon():
    pokemon_name = request.form.get('pokemon_name')
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    if pokemon_name and rating and comment:
        rating = int(rating)
        if rating >= 1 and rating <= 5:
            if save_review_to_database(pokemon_name, rating, comment, user_ip, user_agent):
                return redirect(url_for('pokemon', pokemon_name=pokemon_name))
            else:
                return "Failed to save review to database."
        else:
            return "Please provide a rating between 1 and 5."
    else:
        return "Please provide Pokémon name, rating, and comment."


# Menampilkan halaman filter berdasarkan tipe Pokemon
@app.route("/filter/type/<type_name>")
def filter_by_type(type_name):
    try:
        filtered_pokemon = get_list_pokemon(type_name)
        return render_template("filter.html", pokemon_list=filtered_pokemon)
    except Exception as e:
        return f"Error fetching Pokémon data: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)

# # Menampilkan halaman utama
# @app.route('/')
# def dashboard():
#     all_type = get_all_pokemon_all_type()
#     featured_pokemon = get_top_list_pokemon()[:20]
#     return jsonify({"all_type": all_type, "featured_pokemon": featured_pokemon})

# # Menampilkan hasil pencarian Pokemon dan detail Pokemon
# @app.route('/pokemon', methods=['GET', 'POST'])
# @app.route('/pokemon/<pokemon_name>', methods=['GET', 'POST'])
# def pokemon(pokemon_name=None):
#     if request.method == 'POST':
#         query = request.form.get('pokemon_name')
#         if not query:
#             return jsonify({"error": "Please enter a Pokémon name."})

#         result = get_pokemon_by_name(query)
#         if result:
#             characteristic_id = get_characteristic_id(result['name'])
#             description = get_pokemon_description(characteristic_id)
#             result['description'] = description
#             return jsonify({"pokemon": result, "pokemon_reviews": pokemon_reviews})
#         else:
#             return jsonify({"error": "Invalid Pokémon name."})

#     if pokemon_name:
#         pokemon_detail = get_pokemon_by_name(pokemon_name)
#         if pokemon_detail:
#             characteristic_id = get_characteristic_id(pokemon_detail['name'])
#             description = get_pokemon_description(characteristic_id)
#             pokemon_detail['description'] = description
#             return jsonify({"pokemon": pokemon_detail, "pokemon_reviews": pokemon_reviews})
#         else:
#             return jsonify({"error": "Pokémon not found."})

#     return jsonify({"all_type": get_all_pokemon_all_type()})


# @app.route('/rate', methods=['POST'])
# def rate_pokemon():
#     pokemon_name = request.form.get('pokemon_name')
#     rating = request.form.get('rating')
#     comment = request.form.get('comment')
#     user_ip = request.remote_addr
#     user_agent = request.headers.get('User-Agent')

#     if pokemon_name and rating and comment:
#         rating = int(rating)
#         if rating >= 1 and rating <= 5:
#             pokemon_reviews.append({
#                 'pokemon_name': pokemon_name,
#                 'rating': rating,
#                 'comment': comment,
#                 'user_ip': user_ip,
#                 'user_agent': user_agent
#             })
#             return jsonify({"message": "Rating submitted successfully."})
#         else:
#             return jsonify({"error": "Please provide a rating between 1 and 5."})
#     else:
#         return jsonify({"error": "Please provide Pokémon name, rating, and comment."})
    

# # Menampilkan halaman filter berdasarkan tipe Pokemon
# @app.route("/filter/type/<type_name>")
# def filter_by_type(type_name):
#     try:
#         filtered_pokemon = get_list_pokemon(type_name)
#         return jsonify({"pokemon_list": filtered_pokemon})
#     except Exception as e:
#         return jsonify({"error": f"Error fetching Pokémon data: {str(e)}"})

# if __name__ == '__main__':
#     app.run()