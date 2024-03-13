// Dalam SearchBar.js
import React from 'react';
import './styles/SearchBar.css'; // Sesuaikan dengan styling Anda

function SearchBar({ onSearch }) {
  return (
    <input
      className="search-bar"
      type="search"
      placeholder="Search"
      onChange={(e) => onSearch(e.target.value)}
    />
  );
}

export default SearchBar;