import React, { useState } from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { useApi } from '../../hooks/useApi';
import { api } from '../../api/client';
import LoadingSpinner from '../common/LoadingSpinner';
import './StrategyComparison.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const StrategyComparison = () => {
  const { data, loading, error } = useApi(api.getStrategies);
  const [view, setView] = useState('cost'); // cost, carbon, latency

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="compare-error">Failed to load strategies</div>;
  if (!data) return <div className="compare-empty">No strategy data available</div>;

  const chartData = {
    labels: data.names || ['Baseline', 'Cost-First', 'Weighted'],
    datasets: [
      {
        label: view === 'cost' ? 'Cost ($)' : view === 'carbon' ? 'Carbon (tCO₂)' : 'Latency (ms)',
        data: data[view] || [0, 0, 0],
        backgroundColor: [
          'rgba(96, 165, 250, 0.8)',
          'rgba(52, 211, 153, 0.8)',
          'rgba(167, 139, 250, 0.8)',
        ],
        borderColor: [
          'rgb(96, 165, 250)',
          'rgb(52, 211, 153)',
          'rgb(167, 139, 250)',
        ],
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: 'rgba(17, 24, 39, 0.9)',
        borderColor: 'rgba(148, 163, 184, 0.2)',
        borderWidth: 1,
        titleColor: 'rgb(226, 232, 240)',
        bodyColor: 'rgb(148, 163, 184)',
      },
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(148, 163, 184, 0.05)',
        },
        ticks: {
          color: 'rgba(148, 163, 184, 0.6)',
        },
      },
      y: {
        grid: {
          color: 'rgba(148, 163, 184, 0.05)',
        },
        ticks: {
          color: 'rgba(148, 163, 184, 0.6)',
        },
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="strategy-comparison">
      <div className="compare-header">
        <h3>Strategy Comparison</h3>
        <div className="compare-controls">
          <button
            className={`compare-btn ${view === 'cost' ? 'active' : ''}`}
            onClick={() => setView('cost')}
          >
            Cost
          </button>
          <button
            className={`compare-btn ${view === 'carbon' ? 'active' : ''}`}
            onClick={() => setView('carbon')}
          >
            Carbon
          </button>
          <button
            className={`compare-btn ${view === 'latency' ? 'active' : ''}`}
            onClick={() => setView('latency')}
          >
            Latency
          </button>
        </div>
      </div>
      <div className="chart-container">
        <Bar data={chartData} options={options} />
      </div>
    </div>
  );
};

export default StrategyComparison;