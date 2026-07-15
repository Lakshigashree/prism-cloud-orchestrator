import React from 'react';
import { motion } from 'framer-motion';
import { FiActivity, FiDollarSign, FiCloud, FiZap } from 'react-icons/fi';
import MetricCard from '../components/dashboard/MetricCard';
import LiveTrafficChart from '../components/dashboard/LiveTrafficChart';
import DecisionPanel from '../components/dashboard/DecisionPanel';
import StatsBar from '../components/dashboard/StatsBar';
import './DashboardPage.css';

const DashboardPage = () => {
  const metrics = [
    { title: 'CPU Usage', value: '67%', icon: '📊', color: '#60a5fa', change: 8 },
    { title: 'Active Nodes', value: '12', icon: '🖥️', color: '#34d399', change: 2 },
    { title: 'Carbon Emissions', value: '2.4 tCO₂', icon: '🌍', color: '#a78bfa', change: -5 },
    { title: 'Avg Latency', value: '142 ms', icon: '⚡', color: '#f472b6', change: 12 },
  ];

  return (
    <motion.div 
      className="dashboard-page"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div className="page-header">
        <h2>Dashboard</h2>
        <span className="page-subtitle">Live overview of your cloud orchestration</span>
      </div>

      <div className="metrics-grid">
        {metrics.map((metric, index) => (
          <MetricCard key={index} {...metric} />
        ))}
      </div>

      <StatsBar />

      <div className="dashboard-grid">
        <div className="chart-section">
          <LiveTrafficChart />
        </div>
        <div className="decision-section">
          <DecisionPanel />
        </div>
      </div>
    </motion.div>
  );
};

export default DashboardPage;