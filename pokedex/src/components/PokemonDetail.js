import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './styles/PokemonDetail.css';

// Komponen untuk menampilkan bintang rating
const StarRating = ({ rating }) => {
  const fullStars = '★'.repeat(rating);
  const emptyStars = '☆'.repeat(5 - rating);
  return <div className="star-rating">{fullStars}{emptyStars}</div>;
};

const StarRatingReview = ({ rating }) => {
  const fullStars = '★'.repeat(rating);
  const emptyStars = '☆'.repeat(5 - rating);
  return <div className="star-rating-review">{fullStars}{emptyStars}</div>;
};

// Komponen form untuk submit review baru
const ReviewForm = ({ onReviewSubmit }) => {
  const [reviewText, setReviewText] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    onReviewSubmit(reviewText);
    setReviewText(''); // Reset review text setelah submit
  };

  return (
    <div className="review-form">
      <form onSubmit={handleSubmit}>
        <textarea
          value={reviewText}
          onChange={(e) => setReviewText(e.target.value)}
          placeholder="Ketikkan komentar Anda tentang Pokémon..."
        />
        <button type="submit">Kirim</button>
      </form>
    </div>
  );
};

// Komponen utama detail Pokémon
const PokemonDetail = () => {
  const navigate = useNavigate(); // Hook untuk navigasi
  const { pokemonId } = useParams();
  const [pokemon, setPokemon] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [reviews, setReviews] = useState([]);

  // Fetch data Pokémon dari PokeAPI
  useEffect(() => {
    const fetchPokemonData = async () => {
      setIsLoading(true);
      try {
        // Fetch data Pokémon
        const response = await fetch(`https://pokeapi.co/api/v2/pokemon/${pokemonId}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();

        // Fetch data species untuk mendapatkan deskripsi
        const speciesResponse = await fetch(data.species.url);
        if (!speciesResponse.ok) {
          throw new Error('Network response was not ok');
        }
        const speciesData = await speciesResponse.json();
        const englishDescription = speciesData.flavor_text_entries.find((entry) => entry.language.name === 'en');

        setPokemon({
          ...data,
          description: englishDescription ? englishDescription.flavor_text.replace(/[\n\f]/g, ' ') : "No description available."
        });
      } catch (error) {
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPokemonData();
  }, [pokemonId]);

  // Fungsi untuk menambahkan review baru
  const handleReviewSubmit = (review) => {
    setReviews(prevReviews => [...prevReviews, review]);
  };

  // Fungsi untuk kembali ke halaman utama
  const handleBackClick = () => {
    navigate('/'); // Navigasi ke root/home page
  };

  // Tampilkan pesan loading atau error
  if (isLoading) return <div>Memuat...</div>;
  if (error) return <div>Error: {error}</div>;

  // Render detail Pokémon dan review
  return (
    <div className="pokemon-detail-container">
        <div className="pokemon-deskripsi-container">
          <button onClick={handleBackClick} className="back-button">Back</button>
            <div className="left-column">
                <h1 className="pokemon-name">#{pokemon?.id.toString().padStart(3, '0')} {pokemon?.name}</h1>
                <img className="pokemon-image" src={pokemon?.sprites?.front_default} alt={pokemon?.name} />
            </div>
            <div className="right-column">
                <h2 className='pokemon-description-head'>Description</h2>
                <p className="pokemon-description">{pokemon?.description}</p>
                <h2 className='pokemon-description-head'>Type</h2>
                <div className="pokemon-type">
                    {pokemon?.types?.map((typeInfo) => (
                        <span key={typeInfo.type.name} className="type">
                            {typeInfo.type.name}
                        </span>
                    ))}
                </div>
                <StarRating rating={4} />
            </div>
        </div>

        <div className="pokemon-review-container">
            <ReviewForm onReviewSubmit={handleReviewSubmit} />
            <div className="review-list">
                <h2>Review</h2>
                {reviews.map((review, index) => (
                <div key={index} className="review-item">
                    <p>{review}</p>
                    <StarRatingReview rating={5} /> {/* Setiap review diberi rating 5 untuk contoh */}
                </div>
                ))}
            </div>
        </div>
    </div>
  );
};

export default PokemonDetail;