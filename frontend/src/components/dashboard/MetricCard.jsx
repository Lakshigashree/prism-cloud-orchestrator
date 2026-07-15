import React from 'react';
import { motion } from 'framer-motion';
import './MetricCard.css';

const MetricCard = ({ title, value, icon, change, color, subtitle }) => {
  return (
    <motion.div 
      className="metric-card"
      whileHover={{ y: -4 }}
      transition={{ duration: 0.2 }}
    >
      <div className="metric-header">
        <span className="metric-icon" style={{ color }}>{icon}</span>
        <span className="metric-title">{title}</span>
      </div>
      <div className="metric-value">{value}</div>
      {subtitle && <div className="metric-subtitle">{subtitle}</div>}
      {change !== undefined && (
        <div className={`metric-change ${change >= 0 ? 'positive' : 'negative'}`}>
          {change >= 0 ? '↑' : '↓'} {Math.abs(change)}%
        </div>
      )}
    </motion.div>
  );
};

export default MetricCard;