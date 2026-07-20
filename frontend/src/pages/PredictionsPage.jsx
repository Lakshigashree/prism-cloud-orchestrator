import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import PredictionChart from '../components/dashboard/PredictionChart';
import { useApi } from '../hooks/useApi';
import { api } from '../api/client';
import './PredictionsPage.css';

const PredictionsPage = () => {
  const { data: predictionData, loading, error } = useApi(api.getPredictions, { horizon: 6 });
  const [prediction, setPrediction] = useState(null);

  useEffect(() => {
    if (predictionData) {
      setPrediction(predictionData.data || predictionData);
    }
  }, [predictionData]);

  if (error) {
    return (
      <motion.div 
        className="predictions-page"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <div className="page-header">
          <h2>Predictions</h2>
          <span className="page-subtitle" style={{ color: 'var(--color-red)' }}>
            Error loading predictions
          </span>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div 
      className="predictions-page"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div className="page-header">
        <h2>Predictions</h2>
        <span className="page-subtitle">ARIMA-based traffic forecasting</span>
      </div>

      <div className="prediction-grid">
        <div className="chart-full">
          <PredictionChart data={prediction} loading={loading} />
        </div>
        
        <div className="prediction-info">
          <div className="info-card">
            <h4>Model Details</h4>
            <ul>
              <li><span>Type:</span> {prediction?.method === 'ARIMA' ? 'ARIMA' : 'Moving Average'}</li>
              <li><span>Horizon:</span> {prediction?.horizon_minutes || 30} minutes</li>
              <li><span>Steps:</span> {prediction?.steps || 6}</li>
              <li><span>Trend:</span> {prediction?.trend || 'steady'}</li>
            </ul>
          </div>
          <div className="info-card">
            <h4>Forecast Summary</h4>
            {loading ? (
              <div className="forecast-loading">Loading predictions...</div>
            ) : prediction?.predicted_traffic?.length > 0 ? (
              <>
                <div className="forecast-item">
                  <span>Current Traffic</span>
                  <span className="forecast-value">{prediction.current_value || 0} req/s</span>
                </div>
                <div className="forecast-item">
                  <span>Next 15 min</span>
                  <span className="forecast-value">
                    {prediction.predicted_traffic[0] || 0} req/s
                  </span>
                </div>
                <div className="forecast-item">
                  <span>Next 30 min</span>
                  <span className="forecast-value">
                    {prediction.predicted_traffic[2] || 0} req/s
                  </span>
                </div>
                <div className="forecast-item">
                  <span>Next 60 min</span>
                  <span className="forecast-value">
                    {prediction.predicted_traffic[5] || 0} req/s
                  </span>
                </div>
                <div className="forecast-item" style={{ borderTop: '1px solid var(--border-color)', paddingTop: '0.5rem', marginTop: '0.25rem' }}>
                  <span style={{ fontWeight: 'bold' }}>Trend</span>
                  <span className="forecast-value" style={{ 
                    color: prediction.trend === 'rising' ? 'var(--color-red)' : 
                           prediction.trend === 'falling' ? 'var(--color-green)' : 
                           'var(--color-yellow)'
                  }}>
                    {prediction.trend?.toUpperCase() || 'STEADY'}
                  </span>
                </div>
              </>
            ) : (
              <div className="forecast-empty">No predictions available</div>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default PredictionsPage;