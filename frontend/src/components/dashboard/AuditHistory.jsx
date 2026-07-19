import React, { useState, useEffect } from 'react';
import { useApi } from '../../hooks/useApi';
import { api } from '../../api/client';
import LoadingSpinner from '../common/LoadingSpinner';
import { formatDate, formatTimeAgo } from '../../utils/formatters';
import './AuditHistory.css';

const AuditHistory = () => {
  const { data, loading, error } = useApi(api.getAuditHistory);
  const [entries, setEntries] = useState([]);
  console.log('AuditHistory data:', data);

  useEffect(() => {
    if (data?.entries) {
      setEntries(data.entries.slice(0, 10));
    }
  }, [data]);

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="audit-error">Failed to load audit history</div>;

  return (
    <div className="audit-history">
      <div className="audit-header">
        <h3>Decision History</h3>
        <span className="audit-count">{entries.length} recent entries</span>
      </div>

      <div className="audit-list">
        {entries.length === 0 ? (
          <div className="audit-empty">No decisions recorded yet</div>
        ) : (
          entries.map((entry, index) => (
            <div key={index} className="audit-item">
              <div className="audit-time">{formatTimeAgo(entry.timestamp)}</div>
              <div className="audit-details">
                <span className="audit-action">{entry.action}</span>
                <span className="audit-strategy">{entry.strategy}</span>
              </div>
              <div className="audit-impact">
                <span className="impact-cost">${entry.cost?.toFixed(2)}</span>
                <span className="impact-carbon">{entry.carbon?.toFixed(2)} tCO₂</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default AuditHistory;