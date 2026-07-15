import React from 'react';
import { motion } from 'framer-motion';
import AuditHistory from '../components/dashboard/AuditHistory';
import StatsBar from '../components/dashboard/StatsBar';
import './AuditPage.css';

const AuditPage = () => {
  return (
    <motion.div 
      className="audit-page"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div className="page-header">
        <h2>Audit Trail</h2>
        <span className="page-subtitle">Complete decision history with impact analysis</span>
      </div>

      <StatsBar />

      <div className="audit-grid">
        <AuditHistory />
      </div>
    </motion.div>
  );
};

export default AuditPage;