import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { FiActivity, FiDollarSign, FiCloud, FiZap } from 'react-icons/fi';
import MetricCard from '../components/dashboard/MetricCard';
import LiveTrafficChart from '../components/dashboard/LiveTrafficChart';
import DecisionPanel from '../components/dashboard/DecisionPanel';
import StatsBar from '../components/dashboard/StatsBar';
import { useApi } from '../hooks/useApi';
import { api } from '../api/client';
import './DashboardPage.css';

const DashboardPage = () => {
  const { data: metricsData, loading, error } = useApi(api.getLiveMetrics);
  const [metrics, setMetrics] = useState([
    { title: 'CPU Usage', value: '--', icon: '📊', color: '#60a5fa', change: 0 },
    { title: 'Active Nodes', value: '--', icon: '🖥️', color: '#34d399', change: 0 },
    { title: 'Carbon Emissions', value: '--', icon: '🌍', color: '#a78bfa', change: 0 },
    { title: 'Avg Latency', value: '--', icon: '⚡', color: '#f472b6', change: 0 },
  ]);

  useEffect(() => {
    if (metricsData) {
      const data = metricsData.data || metricsData;
      setMetrics([
        { 
          title: 'CPU Usage', 
          value: `${data.cpu_usage || 0}%`, 
          icon: '📊', 
          color: '#60a5fa', 
          change: data.cpu_usage ? Math.round(data.cpu_usage / 10) : 0 
        },
        { 
          title: 'Active Nodes', 
          value: `${data.active_nodes || 0}`, 
          icon: '🖥️', 
          color: '#34d399', 
          change: 0 
        },
        { 
          title: 'Carbon Emissions', 
          value: `${data.carbon_intensity || 0} gCO₂`, 
          icon: '🌍', 
          color: '#a78bfa', 
          change: 0 
        },
        { 
          title: 'Avg Latency', 
          value: `${data.latency_ms || 0} ms`, 
          icon: '⚡', 
          color: '#f472b6', 
          change: 0 
        },
      ]);
    }
  }, [metricsData]);

  if (loading) {
    return (
      <div className="dashboard-page">
        <div className="page-header">
          <h2>Dashboard</h2>
          <span className="page-subtitle">Loading metrics...</span>
        </div>
        <div className="loading-container">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-page">
        <div className="page-header">
          <h2>Dashboard</h2>
          <span className="page-subtitle" style={{ color: 'var(--color-red)' }}>
            Error: {error}
          </span>
        </div>
      </div>
    );
  }

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