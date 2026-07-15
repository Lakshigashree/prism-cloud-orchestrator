import React, { useState } from 'react';
import { useApi } from '../../hooks/useApi';
import { api } from '../../api/client';
import LoadingSpinner from '../common/LoadingSpinner';
import { FiTrendingUp, FiDollarSign, FiCloud, FiZap } from 'react-icons/fi';
import './DecisionPanel.css';

const DecisionPanel = () => {
  const [strategy, setStrategy] = useState('weighted');
  const { data, loading, error, execute } = useApi(api.getDecision, { strategy });
  const [selectedStrategy, setSelectedStrategy] = useState('weighted');

  const strategies = [
    { id: 'baseline', label: 'Baseline', icon: FiZap, color: '#60a5fa' },
    { id: 'cost', label: 'Cost-First', icon: FiDollarSign, color: '#34d399' },
    { id: 'weighted', label: 'Weighted', icon: FiTrendingUp, color: '#a78bfa' },
  ];

  const handleStrategyChange = (id) => {
    setSelectedStrategy(id);
    execute({ strategy: id });
  };

  const getDecisionColor = (type) => {
    const map = {
      scale_up: 'var(--color-green)',
      scale_down: 'var(--color-red)',
      maintain: 'var(--color-yellow)',
    };
    return map[type] || 'var(--color-blue)';
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="panel-error">Failed to load decision</div>;

  return (
    <div className="decision-panel">
      <div className="panel-header">
        <h3>Live Decision Engine</h3>
        <div className="strategy-tabs">
          {strategies.map((s) => (
            <button
              key={s.id}
              className={`strategy-tab ${selectedStrategy === s.id ? 'active' : ''}`}
              onClick={() => handleStrategyChange(s.id)}
            >
              <s.icon size={14} />
              {s.label}
            </button>
          ))}
        </div>
      </div>

      {data && (
        <div className="decision-content">
          <div className="decision-main">
            <div 
              className="decision-action"
              style={{ borderColor: getDecisionColor(data.action) }}
            >
              <span className="action-label">Recommended Action</span>
              <span className="action-value">{data.action?.toUpperCase() || 'Maintain'}</span>
            </div>
            
            <div className="decision-metrics">
              <div className="metric-item">
                <span className="metric-label">Cost Impact</span>
                <span className="metric-value">${data.impact?.cost?.toFixed(2) || '—'}</span>
              </div>
              <div className="metric-item">
                <span className="metric-label">Carbon Impact</span>
                <span className="metric-value">{data.impact?.carbon?.toFixed(2) || '—'} tCO₂</span>
              </div>
              <div className="metric-item">
                <span className="metric-label">Latency Impact</span>
                <span className="metric-value">{data.impact?.latency?.toFixed(0) || '—'} ms</span>
              </div>
            </div>
          </div>

          <div className="decision-explanation">
            <h4>Explanation</h4>
            <p>{data.explanation || 'No explanation available'}</p>
          </div>

          <div className="decision-weights">
            <h4>Current Weights</h4>
            <div className="weights-bars">
              <div className="weight-item">
                <span>Cost</span>
                <div className="weight-bar">
                  <div 
                    className="weight-fill" 
                    style={{ width: `${(data.weights?.cost || 0.33) * 100}%`, background: '#34d399' }}
                  />
                </div>
                <span className="weight-value">{((data.weights?.cost || 0.33) * 100).toFixed(0)}%</span>
              </div>
              <div className="weight-item">
                <span>Carbon</span>
                <div className="weight-bar">
                  <div 
                    className="weight-fill" 
                    style={{ width: `${(data.weights?.carbon || 0.33) * 100}%`, background: '#60a5fa' }}
                  />
                </div>
                <span className="weight-value">{((data.weights?.carbon || 0.33) * 100).toFixed(0)}%</span>
              </div>
              <div className="weight-item">
                <span>Latency</span>
                <div className="weight-bar">
                  <div 
                    className="weight-fill" 
                    style={{ width: `${(data.weights?.latency || 0.34) * 100}%`, background: '#a78bfa' }}
                  />
                </div>
                <span className="weight-value">{((data.weights?.latency || 0.34) * 100).toFixed(0)}%</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DecisionPanel;