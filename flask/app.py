from flask import Flask, request, jsonify
import requests
# import mysql.connector

app = Flask(_name_)

# Fungsi untuk koneksi ke database
# def connect_to_database():
#     try:
#         connection = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password='',
#             database='pokedexapp'
#         )
#         return connection
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#         return None

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

# Menyimpan rating dan komentar Pokemon
pokemon_reviews = []

# Menampilkan halaman utama
@app.route('/')
def dashboard():
    all_type = get_all_pokemon_all_type()
    featured_pokemon = get_top_list_pokemon()[:20]
    return jsonify({"all_type": all_type, "featured_pokemon": featured_pokemon})


# Menampilkan hasil pencarian Pokemon dan detail Pokemon
@app.route('/pokemon', methods=['GET', 'POST'])
@app.route('/pokemon/<pokemon_name>', methods=['GET', 'POST'])
def pokemon(pokemon_name=None):
    if request.method == 'POST':
        query = request.form.get('pokemon_name')
        if not query:
            return jsonify({"error": "Please enter a Pokémon name."})

        result = get_pokemon_by_name(query)
        if result:
            characteristic_id = get_characteristic_id(result['name'])
            description = get_pokemon_description(characteristic_id)
            result['description'] = description
            return jsonify({"pokemon": result, "pokemon_reviews": pokemon_reviews})
        else:
            return jsonify({"error": "Invalid Pokémon name."})

    if pokemon_name:
        pokemon_detail = get_pokemon_by_name(pokemon_name)
        if pokemon_detail:
            characteristic_id = get_characteristic_id(pokemon_detail['name'])
            description = get_pokemon_description(characteristic_id)
            pokemon_detail['description'] = description
            return jsonify({"pokemon": pokemon_detail, "pokemon_reviews": pokemon_reviews})
        else:
            return jsonify({"error": "Pokémon not found."})

    return jsonify({"all_type": get_all_pokemon_all_type()})


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
            pokemon_reviews.append({
                'pokemon_name': pokemon_name,
                'rating': rating,
                'comment': comment,
                'user_ip': user_ip,
                'user_agent': user_agent
            })
            return jsonify({"message": "Rating submitted successfully."})
        else:
            return jsonify({"error": "Please provide a rating between 1 and 5."})
    else:
        return jsonify({"error": "Please provide Pokémon name, rating, and comment."})
    
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

# Menampilkan halaman filter berdasarkan tipe Pokemon
@app.route("/filter/type/<type_name>")
def filter_by_type(type_name):
    try:
        filtered_pokemon = get_list_pokemon(type_name)
        return jsonify({"pokemon_list": filtered_pokemon})
    except Exception as e:
        return jsonify({"error": f"Error fetching Pokémon data: {str(e)}"})

if _name_ == '_main_':
    app.run(debug=True)