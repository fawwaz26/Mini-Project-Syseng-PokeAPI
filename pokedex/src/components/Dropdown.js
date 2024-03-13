// Dalam Dropdown.js
import React from 'react';
import './styles/Dropdown.css'; // Sesuaikan dengan styling Anda

function Dropdown({ onCategoryChange, categories }) {
  return (
    <select className="dropdown" onChange={(e) => onCategoryChange(e.target.value)}>
      {categories.map((category) => (
        <option key={category} value={category}>{category}</option>
      ))}
    </select>
  );
}

export default Dropdown;