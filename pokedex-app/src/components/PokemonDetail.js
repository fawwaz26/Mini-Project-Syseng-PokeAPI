import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './styles/PokemonDetail.css'; 

function PokemonDetail() {
  const { pokemonName } = useParams();
  const [pokemonDetails, setPokemonDetails] = useState(null);

  useEffect(() => {
    async function fetchPokemonDetails() {
      try {
        const response = await fetch(`https://pokeapi.co/api/v2/pokemon/${pokemonName}`);
        const details = await response.json();
        setPokemonDetails(details);
      } catch (error) {
        console.error("Error fetching details:", error);
      }
    }

    fetchPokemonDetails();
  }, [pokemonName]);

  if (!pokemonDetails) {
    return <div>Loading...</div>; // Handle loading state
  }

  // Now you have `pokemonDetails` to use in your JSX
  return (
    <div className="pokemon-detail">
      {/* Render the UI with pokemonDetails */}
      {/* You'll need to format the details to match your design */}
    </div>
  );
}

export default PokemonDetail;
