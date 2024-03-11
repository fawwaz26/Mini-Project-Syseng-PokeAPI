// Dalam Card.js
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './styles/Card.css'; // Sesuaikan dengan styling Anda

function Card({ name, url }) {
  const [pokemonDetails, setPokemonDetails] = useState(null);

  useEffect(() => {
    async function fetchPokemonDetails() {
      try {
        const response = await fetch(url);
        const details = await response.json();
        setPokemonDetails(details);
      } catch (error) {
        console.error("Error fetching details: ", error);
      }
    }

    fetchPokemonDetails();
  }, [url]); // URL sebagai dependensi, sehingga jika berubah, akan mengambil data baru

  if (!pokemonDetails) {
    return <div>Loading...</div>; // Atau tampilkan placeholder lainnya
  }

  // Dapatkan URL gambar Pokémon
  const imageUrl = pokemonDetails.sprites?.front_default;

  return (
    <div className="card">
      <div className="card-image">
        <img src={imageUrl} alt={name} />
      </div>
      <div className="card-info">
        <h3>{name}</h3>
        <p>{`#${pokemonDetails.id.toString().padStart(3, '0')}`}</p>
        <div className="card-types">
          {pokemonDetails.types.map((typeInfo) => (
            <span key={typeInfo.type.name} className="type">
              {typeInfo.type.name}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Card;