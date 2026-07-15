import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || '/api';

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API endpoints
export const api = {
  // Monitoring
  getLiveMetrics: () => apiClient.get('/monitoring/live'),
  getTraffic: () => apiClient.get('/traffic'),
  
  // Carbon
  getCarbonData: () => apiClient.get('/carbon'),
  
  // Predictions
  getPredictions: (params) => apiClient.get('/prediction', { params }),
  
  // Decisions
  getDecision: (params) => apiClient.get('/decision', { params }),
  getStrategies: () => apiClient.get('/decision/strategies'),
  
  // Audit
  getAuditHistory: (params) => apiClient.get('/audit/history', { params }),
  getAuditStats: () => apiClient.get('/audit/stats'),
  
  // Results
  getResults: () => apiClient.get('/results'),
};

export default apiClient;