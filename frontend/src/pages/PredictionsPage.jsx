import React from 'react';
import { motion } from 'framer-motion';
import PredictionChart from '../components/dashboard/PredictionChart';
import './PredictionsPage.css';

const PredictionsPage = () => {
  return (
    <motion.div 
      className="predictions-page"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div className="page-header">
        <h2>Predictions</h2>
        <span className="page-subtitle">LSTM-based traffic forecasting</span>
      </div>

      <div className="prediction-grid">
        <div className="chart-full">
          <PredictionChart />
        </div>
        
        <div className="prediction-info">
          <div className="info-card">
            <h4>Model Details</h4>
            <ul>
              <li><span>Type:</span> LSTM Neural Network</li>
              <li><span>Sequence Length:</span> 60 minutes</li>
              <li><span>Features:</span> CPU, Requests, Latency</li>
              <li><span>Accuracy:</span> 92.3%</li>
            </ul>
          </div>
          <div className="info-card">
            <h4>Forecast Summary</h4>
            <div className="forecast-item">
              <span>Next 15 min</span>
              <span className="forecast-value">↑ 12%</span>
            </div>
            <div className="forecast-item">
              <span>Next 30 min</span>
              <span className="forecast-value">↑ 8%</span>
            </div>
            <div className="forecast-item">
              <span>Next 60 min</span>
              <span className="forecast-value">→ 3%</span>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default PredictionsPage;