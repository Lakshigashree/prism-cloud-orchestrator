export const formatNumber = (num, decimals = 2) => {
  if (num === undefined || num === null) return '—';
  return Number(num).toFixed(decimals);
};

export const formatCurrency = (num) => {
  if (num === undefined || num === null) return '—';
  return '$' + Number(num).toFixed(2);
};

export const formatCarbon = (num) => {
  if (num === undefined || num === null) return '—';
  return Number(num).toFixed(2) + ' tCO₂';
};

export const formatLatency = (num) => {
  if (num === undefined || num === null) return '—';
  return Number(num).toFixed(0) + ' ms';
};

export const formatDate = (timestamp) => {
  if (!timestamp) return '—';
  const date = new Date(timestamp);
  return date.toLocaleString();
};

export const formatTimeAgo = (timestamp) => {
  if (!timestamp) return '—';
  const diff = Date.now() - new Date(timestamp).getTime();
  const minutes = Math.floor(diff / 60000);
  if (minutes < 1) return 'Just now';
  if (minutes < 60) return minutes + 'm ago';
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return hours + 'h ago';
  return Math.floor(hours / 24) + 'd ago';
};

export const getStatusColor = (value, thresholds) => {
  if (!thresholds) return 'var(--color-blue)';
  if (value >= thresholds.danger) return 'var(--color-red)';
  if (value >= thresholds.warning) return 'var(--color-yellow)';
  return 'var(--color-green)';
};