import React from 'react';
import { useApi } from '../../hooks/useApi';
import { api } from '../../api/client';
import LoadingSpinner from '../common/LoadingSpinner';
import './StatsBar.css';

const StatsBar = () => {
  const { data, loading, error } = useApi(api.getAuditStats);

  if (loading) return <LoadingSpinner size="small" />;
  if (error || !data) return null;

  // Extract data from API response
  const statsData = data.data || data;

  const stats = [
    { label: 'Total Decisions', value: statsData.total_decisions || 0 },
    { label: 'Cost Saved', value: `$${statsData.total_cost_saved?.toFixed(2) || '0'}` },
    { label: 'Carbon Saved', value: `${statsData.total_carbon_saved?.toFixed(2) || '0'} tCO₂` },
    { label: 'Avg Latency', value: `${statsData.average_latency?.toFixed(0) || '0'} ms` },
  ];

  return (
    <div className="stats-bar">
      {stats.map((stat, index) => (
        <div key={index} className="stat-item">
          <span className="stat-label">{stat.label}</span>
          <span className="stat-value">{stat.value}</span>
        </div>
      ))}
    </div>
  );
};

export default StatsBar;