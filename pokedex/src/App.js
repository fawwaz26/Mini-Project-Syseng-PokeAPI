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

    fetchPokemons();
  }, []);

  function handleSearch(value) {
    // Implementasikan logika pencarian
  }

  function handleCategoryChange(category) {
    // Implementasikan logika filter kategori
  }

  return (
    <Router>
      <div className="App">
        <header>
          <img src={logo} alt="Pokédex" />
        </header>
        <search>
          <SearchBar onSearch={handleSearch} />
          <Dropdown onCategoryChange={handleCategoryChange} categories={['All', 'Grass', 'Poison']} />
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