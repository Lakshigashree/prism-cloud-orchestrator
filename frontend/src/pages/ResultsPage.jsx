import React from 'react';
import { motion } from 'framer-motion';
import StrategyComparison from '../components/dashboard/StrategyComparison';
import './ResultsPage.css';

const ResultsPage = () => {
  return (
    <motion.div 
      className="results-page"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div className="page-header">
        <h2>Results</h2>
        <span className="page-subtitle">Strategy comparison and performance analysis</span>
      </div>

      <div className="results-grid">
        <div className="result-card">
          <h3>Performance Comparison</h3>
          <StrategyComparison />
        </div>
        
        <div className="results-summary">
          <div className="summary-card">
            <h4>Key Findings</h4>
            <div className="finding-item">
              <span className="finding-label">Best Cost Performance</span>
              <span className="finding-value">Cost-First Strategy</span>
            </div>
            <div className="finding-item">
              <span className="finding-label">Lowest Carbon</span>
              <span className="finding-value">Weighted Strategy</span>
            </div>
            <div className="finding-item">
              <span className="finding-label">Best Latency</span>
              <span className="finding-value">Baseline Strategy</span>
            </div>
            <div className="finding-item">
              <span className="finding-label">Overall Winner</span>
              <span className="finding-value highlight">Weighted Strategy</span>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default ResultsPage;