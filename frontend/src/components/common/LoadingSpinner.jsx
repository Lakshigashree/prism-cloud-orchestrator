import React from 'react';
import './LoadingSpinner.css';

const LoadingSpinner = ({ size = 'medium' }) => {
  const sizeClass = `spinner-${size}`;
  
  return (
    <div className={`spinner ${sizeClass}`}>
      <div className="spinner-circle"></div>
    </div>
  );
};

export default LoadingSpinner;