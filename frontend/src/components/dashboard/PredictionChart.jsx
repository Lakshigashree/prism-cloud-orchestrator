import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { useApi } from '../../hooks/useApi';
import { api } from '../../api/client';
import LoadingSpinner from '../common/LoadingSpinner';
import './PredictionChart.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const PredictionChart = () => {
  const { data, loading, error } = useApi(api.getPredictions, { horizon: 6 });
  const [chartData, setChartData] = useState(null);
  const [modelInfo, setModelInfo] = useState({ method: 'Loading...', trend: '--' });

  useEffect(() => {
    if (data) {
      // Extract data from API response
      const predictionData = data.data || data;
      
      const historicalValues = predictionData.historical_values || [];
      const predictedValues = predictionData.predicted_traffic || [];
      const historicalTimestamps = predictionData.historical_timestamps || [];
      const futureTimestamps = predictionData.future_timestamps || [];
      
      // Combine for display
      const allLabels = [...historicalTimestamps, ...futureTimestamps];
      
      // Create datasets with null gaps
      const historicalData = [...historicalValues, ...Array(predictedValues.length).fill(null)];
      const predictedData = [...Array(historicalValues.length).fill(null), ...predictedValues];

      setChartData({
        labels: allLabels,
        datasets: [
          {
            label: 'Historical',
            data: historicalData,
            borderColor: 'rgb(96, 165, 250)',
            backgroundColor: 'rgba(96, 165, 250, 0.05)',
            fill: true,
            tension: 0.4,
            pointRadius: 2,
          },
          {
            label: 'Predicted',
            data: predictedData,
            borderColor: 'rgb(244, 114, 182)',
            backgroundColor: 'rgba(244, 114, 182, 0.05)',
            fill: true,
            borderDash: [5, 5],
            tension: 0.4,
            pointRadius: 3,
            pointBackgroundColor: 'rgb(244, 114, 182)',
          },
        ],
      });

      setModelInfo({
        method: predictionData.method || 'Unknown',
        trend: predictionData.trend || 'steady'
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
          maxTicksLimit: 12,
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
    interaction: {
      intersect: false,
      mode: 'index',
    },
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="chart-error">Failed to load predictions</div>;
  if (!chartData) return <div className="chart-empty">No prediction data available</div>;

  return (
    <div className="prediction-chart">
      <div className="chart-header">
        <h3>Traffic Predictions</h3>
        <span className="chart-model">{modelInfo.method} • Trend: {modelInfo.trend}</span>
      </div>
      <div className="chart-container">
        <Line data={chartData} options={options} />
      </div>
    </div>
  );
};

export default PredictionChart;