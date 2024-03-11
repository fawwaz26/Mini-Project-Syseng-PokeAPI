// Dalam App.js
import React, { useState, useEffect } from 'react';
import Card from './components/Card';
import SearchBar from './components/SearchBar';
import Dropdown from './components/Dropdown';
import logo from './logo.png';
import './styles/App.css'; // Sesuaikan dengan styling Anda

function App() {
  const [pokemons, setPokemons] = useState([]); // Akan diisi dengan data dari API atau mock data
  
  useEffect(() => {
    async function fetchPokemons() {
      try {
        const response = await fetch('https://pokeapi.co/api/v2/pokemon?limit=151');
        const data = await response.json();
        setPokemons(data.results);
      } catch (error) {
        console.error("Error fetching data: ", error);
      }
    }

    fetchPokemons();
  }, []);

  // Fungsi untuk menangani pencarian dan filter
  function handleSearch(value) {
    // Implementasikan logika pencarian
  }

  function handleCategoryChange(category) {
    // Implementasikan logika filter kategori
  }

  return (
    <div className="App">
      <header>
        {/* Logo dan komponen pencarian */}
        <img src={logo} alt="Pokédex" />
      </header>
      <search>
        <SearchBar onSearch={handleSearch} />
        <Dropdown onCategoryChange={handleCategoryChange} categories={['All', 'Grass', 'Poison']} />
      </search>
      <main>
        <div className="card-container">
          {pokemons.map((pokemon) => (
            <Card key={pokemon.name} name={pokemon.name} url={pokemon.url} />
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;
