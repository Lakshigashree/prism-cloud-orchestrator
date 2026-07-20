import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import StrategyComparison from '../components/dashboard/StrategyComparison';
import { useApi } from '../hooks/useApi';
import { api } from '../api/client';
import './ResultsPage.css';

const ResultsPage = () => {
  const { data: resultsData, loading, error } = useApi(api.getResults);
  const [results, setResults] = useState(null);
  const [findings, setFindings] = useState({
    bestCost: '--',
    bestCarbon: '--',
    bestLatency: '--',
    overallWinner: '--'
  });

  useEffect(() => {
    if (resultsData) {
      const data = resultsData.data || resultsData;
      setResults(data);
      
      // Calculate findings from data
      if (data.strategies && data.strategies.length > 0) {
        const strategies = data.strategies;
        
        // Find best cost (highest costSaved)
        const bestCost = strategies.reduce((a, b) => 
          (a.costSaved?.reduce((sum, v) => sum + v, 0) || 0) > 
          (b.costSaved?.reduce((sum, v) => sum + v, 0) || 0) ? a : b
        );
        
        // Find best carbon (highest carbonSaved)
        const bestCarbon = strategies.reduce((a, b) => 
          (a.carbonSaved?.reduce((sum, v) => sum + v, 0) || 0) > 
          (b.carbonSaved?.reduce((sum, v) => sum + v, 0) || 0) ? a : b
        );
        
        // Find best latency (lowest latencyPenalty)
        const bestLatency = strategies.reduce((a, b) => 
          (a.latencyPenalty?.reduce((sum, v) => sum + v, 0) || 0) < 
          (b.latencyPenalty?.reduce((sum, v) => sum + v, 0) || 0) ? a : b
        );
        
        // Overall winner: highest combined score
        const overall = strategies.reduce((a, b) => {
          const scoreA = (a.costSaved?.reduce((s, v) => s + v, 0) || 0) + 
                         (a.carbonSaved?.reduce((s, v) => s + v, 0) || 0) - 
                         (a.latencyPenalty?.reduce((s, v) => s + v, 0) || 0) / 10;
          const scoreB = (b.costSaved?.reduce((s, v) => s + v, 0) || 0) + 
                         (b.carbonSaved?.reduce((s, v) => s + v, 0) || 0) - 
                         (b.latencyPenalty?.reduce((s, v) => s + v, 0) || 0) / 10;
          return scoreA > scoreB ? a : b;
        });
        
        setFindings({
          bestCost: bestCost?.name || '--',
          bestCarbon: bestCarbon?.name || '--',
          bestLatency: bestLatency?.name || '--',
          overallWinner: overall?.name || '--'
        });
      }
    }
  }, [resultsData]);

  if (error) {
    return (
      <motion.div 
        className="results-page"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <div className="page-header">
          <h2>Results</h2>
          <span className="page-subtitle" style={{ color: 'var(--color-red)' }}>
            Error loading results
          </span>
        </div>
      </motion.div>
    );
  }

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
          <StrategyComparison strategies={results} loading={loading} />
        </div>
        
        <div className="results-summary">
          <div className="summary-card">
            <h4>Key Findings</h4>
            {loading ? (
              <div className="finding-loading">Loading results...</div>
            ) : (
              <>
                <div className="finding-item">
                  <span className="finding-label">Best Cost Performance</span>
                  <span className="finding-value">{findings.bestCost}</span>
                </div>
                <div className="finding-item">
                  <span className="finding-label">Lowest Carbon</span>
                  <span className="finding-value">{findings.bestCarbon}</span>
                </div>
                <div className="finding-item">
                  <span className="finding-label">Best Latency</span>
                  <span className="finding-value">{findings.bestLatency}</span>
                </div>
                <div className="finding-item">
                  <span className="finding-label">Overall Winner</span>
                  <span className="finding-value highlight">{findings.overallWinner}</span>
                </div>
              </>
            )}
          </div>
          
          {results?.note && (
            <div className="summary-card" style={{ borderColor: 'var(--color-yellow)' }}>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textAlign: 'center' }}>
                📝 {results.note}
              </p>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default ResultsPage;