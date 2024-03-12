import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './styles/Card.css'; // Pastikan path sesuai dengan struktur folder Anda

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
  }, [url]);

  if (!pokemonDetails) {
    return <div>Loading...</div>;
  }

  const imageUrl = pokemonDetails.sprites?.front_default;
  // Gunakan ID atau nama Pokémon sebagai parameter untuk navigasi
  const pokemonId = pokemonDetails.id;

  return (
    <Link to={`/pokemon/${pokemonId}`} style={{ textDecoration: 'none' }}> {/* Style disini untuk menghilangkan underline default dari Link */}
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
    </Link>
  );
}

export default Card;