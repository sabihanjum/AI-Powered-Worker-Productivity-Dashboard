import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getDashboardMetrics = async () => {
  const response = await api.get('/api/metrics/dashboard');
  return response.data;
};

export const getWorkerMetrics = async (workerId = null) => {
  const url = workerId 
    ? `/api/metrics/workers?worker_id=${workerId}`
    : '/api/metrics/workers';
  const response = await api.get(url);
  return response.data;
};

export const getWorkstationMetrics = async (stationId = null) => {
  const url = stationId 
    ? `/api/metrics/workstations?station_id=${stationId}`
    : '/api/metrics/workstations';
  const response = await api.get(url);
  return response.data;
};

export const getFactoryMetrics = async () => {
  const response = await api.get('/api/metrics/factory');
  return response.data;
};

export const getWorkers = async () => {
  const response = await api.get('/api/workers');
  return response.data;
};

export const getWorkstations = async () => {
  const response = await api.get('/api/workstations');
  return response.data;
};

export const seedData = async (days = 7) => {
  const response = await api.post(`/api/admin/seed-data?days=${days}`);
  return response.data;
};

export const ingestEvent = async (event) => {
  const response = await api.post('/api/events', event);
  return response.data;
};

export default api;
