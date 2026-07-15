import React from 'react';
import { motion } from 'framer-motion';
import DecisionPanel from '../components/dashboard/DecisionPanel';
import StrategyComparison from '../components/dashboard/StrategyComparison';
import './DecisionsPage.css';

const DecisionsPage = () => {
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
          <DecisionPanel />
        </div>
        <div className="strategy-section">
          <StrategyComparison />
        </div>
      </div>
    </motion.div>
  );
};

export default DecisionsPage;