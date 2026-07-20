import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import AuditHistory from '../components/dashboard/AuditHistory';
import StatsBar from '../components/dashboard/StatsBar';
import { useApi } from '../hooks/useApi';
import { api } from '../api/client';
import './AuditPage.css';

const AuditPage = () => {
  const { data: statsData, loading: statsLoading, error: statsError } = useApi(api.getAuditStats);
  const { data: historyData, loading: historyLoading, error: historyError } = useApi(api.getAuditHistory);
  
  const [stats, setStats] = useState({
    total_decisions: 0,
    total_cost_saved: 0,
    total_carbon_saved: 0,
    average_latency: 0
  });

  useEffect(() => {
    if (statsData) {
      const data = statsData.data || statsData;
      setStats({
        total_decisions: data.total_decisions || 0,
        total_cost_saved: data.total_cost_saved || 0,
        total_carbon_saved: data.total_carbon_saved || 0,
        average_latency: data.average_latency || 0
      });
    }
  }, [statsData]);

  if (statsError || historyError) {
    return (
      <motion.div 
        className="audit-page"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <div className="page-header">
          <h2>Audit Trail</h2>
          <span className="page-subtitle" style={{ color: 'var(--color-red)' }}>
            Error loading audit data
          </span>
        </div>
      </motion.div>
    );
  }

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

      <StatsBar 
        totalDecisions={stats.total_decisions}
        costSaved={stats.total_cost_saved}
        carbonSaved={stats.total_carbon_saved}
        avgLatency={stats.average_latency}
        loading={statsLoading}
      />

      <div className="audit-grid">
        <AuditHistory entries={historyData?.data?.entries || []} loading={historyLoading} />
      </div>
    </motion.div>
  );
};

export default AuditPage;