import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import PokemonDetail from './components/PokemonDetail';
import Card from './components/Card';
import SearchBar from './components/SearchBar';
import Dropdown from './components/Dropdown';
import logo from './logo.png';
import './styles/App.css'; // Sesuaikan dengan styling Anda

function App() {
  const [pokemons, setPokemons] = useState([]);
  const [categories, setCategories] = useState(['All']); // Awalnya hanya berisi 'All'

  useEffect(() => {
    async function fetchPokemons() {
      try {
        const response = await fetch('https://pokeapi.co/api/v2/pokemon');
        const data = await response.json();
        setPokemons(data.results);
      } catch (error) {
        console.error("Error fetching data: ", error);
      }
    }

    async function fetchCategories() {
      try {
        const response = await fetch('https://pokeapi.co/api/v2/type');
        const data = await response.json();
        setCategories(['All', ...data.results.map(type => type.name)]); // Tambahkan 'All' dan semua tipe ke dalam state
      } catch (error) {
        console.error("Error fetching types: ", error);
      }
    }

    fetchPokemons();
    fetchCategories();
  }, []);

  async function handleSearch(value) {
    if (!value) {
      // Jika string pencarian kosong, tampilkan semua Pokémon
      try {
        const response = await fetch('https://pokeapi.co/api/v2/pokemon?limit=30');
        const data = await response.json();
        setPokemons(data.results);
      } catch (error) {
        console.error("Error fetching all pokemons: ", error);
      }
    } else {
      // Gunakan state pokemons yang ada untuk menyaring berdasarkan nama
      // Ini memerlukan fetching semua Pokémon terlebih dahulu dan menyimpannya di state
      const filteredPokemons = pokemons.filter(pokemon =>
        pokemon.name.toLowerCase().includes(value.toLowerCase())
      );
      setPokemons(filteredPokemons);
    }
  }
  

  async function handleCategoryChange(category) {
    if (category === 'All') {
      // Jika kategori 'All' dipilih, tampilkan semua Pokémon
      try {
        const response = await fetch('https://pokeapi.co/api/v2/pokemon?limit=30');
        const data = await response.json();
        setPokemons(data.results);
      } catch (error) {
        console.error("Error fetching all pokemons: ", error);
      }
    } else {
      // Jika kategori selain 'All' dipilih, filter berdasarkan tipe
      try {
        const response = await fetch(`https://pokeapi.co/api/v2/type/${category}`);
        const data = await response.json();
        const filteredPokemons = data.pokemon.map(p => p.pokemon); // Dapatkan daftar Pokémon dari tipe yang dipilih
        setPokemons(filteredPokemons);
      } catch (error) {
        console.error(`Error fetching pokemons for category ${category}: `, error);
      }
    }
  }
  

  return (
    <Router>
      <div className="App">
        <header>
          <img src={logo} alt="Pokédex" />
        </header>
        <search>
          <SearchBar onSearch={handleSearch} />
          <Dropdown onCategoryChange={handleCategoryChange} categories={categories} />
        </search>
        <main>
          <Routes>
            {/* Rute untuk halaman utama */}
            <Route path="/" element={
              <div className="card-container">
                {pokemons.map((pokemon) => (
                  <Card key={pokemon.name} name={pokemon.name} url={pokemon.url} />
                ))}
              </div>
            } />
            {/* Rute untuk halaman detail Pokémon */}
            <Route path="/pokemon/:pokemonId" element={<PokemonDetail />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;