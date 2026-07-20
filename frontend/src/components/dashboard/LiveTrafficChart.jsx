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
import './LiveTrafficChart.css';

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

const LiveTrafficChart = () => {
  const { data, loading, error } = useApi(api.getTraffic);
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    if (data) {
      // Extract data from API response
      const trafficData = data.data || data;
      const labels = trafficData.timestamps || [];
      const cpuData = trafficData.cpu || [];
      const requestsData = trafficData.requests || [];
      const latencyData = trafficData.latency || [];

      setChartData({
        labels,
        datasets: [
          {
            label: 'CPU Usage (%)',
            data: cpuData,
            borderColor: 'rgb(96, 165, 250)',
            backgroundColor: 'rgba(96, 165, 250, 0.1)',
            fill: true,
            tension: 0.4,
            pointRadius: 2,
          },
          {
            label: 'Requests/s',
            data: requestsData,
            borderColor: 'rgb(167, 139, 250)',
            backgroundColor: 'rgba(167, 139, 250, 0.1)',
            fill: true,
            tension: 0.4,
            pointRadius: 2,
          },
          {
            label: 'Latency (ms)',
            data: latencyData,
            borderColor: 'rgb(244, 114, 182)',
            backgroundColor: 'rgba(244, 114, 182, 0.1)',
            fill: true,
            tension: 0.4,
            pointRadius: 2,
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
        mode: 'index',
        intersect: false,
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
          maxTicksLimit: 15,
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
  if (error) return <div className="chart-error">Failed to load traffic data</div>;
  if (!chartData) return <div className="chart-empty">No data available</div>;

  return (
    <div className="live-traffic-chart">
      <div className="chart-header">
        <h3>Live Traffic Metrics</h3>
        <span className="chart-status">● Live</span>
      </div>
      <div className="chart-container">
        <Line data={chartData} options={options} />
      </div>
    </div>
  );
};

export default LiveTrafficChart;