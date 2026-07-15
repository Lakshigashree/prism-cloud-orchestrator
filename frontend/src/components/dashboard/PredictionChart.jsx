import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { useApi } from '../../hooks/useApi';
import { api } from '../../api/client';
import LoadingSpinner from '../common/LoadingSpinner';
import './PredictionChart.css';

const PredictionChart = () => {
  const { data, loading, error } = useApi(api.getPredictions);
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    if (data) {
      const labels = data.timestamps || [];
      const historical = data.historical || [];
      const predicted = data.predicted || [];

      setChartData({
        labels,
        datasets: [
          {
            label: 'Historical',
            data: historical,
            borderColor: 'rgb(96, 165, 250)',
            backgroundColor: 'rgba(96, 165, 250, 0.05)',
            fill: true,
            tension: 0.4,
          },
          {
            label: 'Predicted',
            data: predicted,
            borderColor: 'rgb(244, 114, 182)',
            backgroundColor: 'rgba(244, 114, 182, 0.05)',
            fill: true,
            borderDash: [5, 5],
            tension: 0.4,
          },
        ],
      });
    }
  }, [data]);

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: 'rgba(148, 163, 184, 0.8)',
          usePointStyle: true,
          pointStyle: 'circle',
        },
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

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="chart-error">Failed to load predictions</div>;
  if (!chartData) return <div className="chart-empty">No prediction data available</div>;

  return (
    <div className="prediction-chart">
      <div className="chart-header">
        <h3>Traffic Predictions</h3>
        <span className="chart-model">LSTM Model</span>
      </div>
      <div className="chart-container">
        <Line data={chartData} options={options} />
      </div>
    </div>
  );
};

export default PredictionChart;