import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import DecisionPanel from '../components/dashboard/DecisionPanel';
import StrategyComparison from '../components/dashboard/StrategyComparison';
import { useApi } from '../hooks/useApi';
import { api } from '../api/client';
import './DecisionsPage.css';

const DecisionsPage = () => {
  const { data: decisionData, loading: decisionLoading, error: decisionError } = useApi(api.getDecision);
  const { data: strategiesData, loading: strategiesLoading, error: strategiesError } = useApi(api.getStrategies);
  
  const [decision, setDecision] = useState(null);
  const [strategies, setStrategies] = useState(null);

  useEffect(() => {
    if (decisionData) {
      setDecision(decisionData.data || decisionData);
    }
  }, [decisionData]);

  useEffect(() => {
    if (strategiesData) {
      setStrategies(strategiesData.data || strategiesData);
    }
  }, [strategiesData]);

  if (decisionError || strategiesError) {
    return (
      <motion.div 
        className="decisions-page"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <div className="page-header">
          <h2>Decisions</h2>
          <span className="page-subtitle" style={{ color: 'var(--color-red)' }}>
            Error loading decision data
          </span>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div 
      className="decisions-page"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div className="page-header">
        <h2>Decisions</h2>
        <span className="page-subtitle">Multi-objective optimization engine</span>
      </div>

      <div className="decisions-grid">
        <div className="decision-main">
          <DecisionPanel decision={decision} loading={decisionLoading} />
        </div>
        <div className="strategy-section">
          <StrategyComparison strategies={strategies} loading={strategiesLoading} />
        </div>
      </div>
    </motion.div>
  );
};

export default DecisionsPage;