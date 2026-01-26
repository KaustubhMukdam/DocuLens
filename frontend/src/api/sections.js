import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance with auth
const apiClient = axios.create({
  baseURL: API_URL,
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Sections API
export const sectionsAPI = {
  getById: async (id) => {
    const { data } = await apiClient.get(`/docs/sections/${id}`);
    return data;
  },
  
  markComplete: async (sectionId, timeSpent, notes) => {
    const { data } = await apiClient.post(`/progress/sections/${sectionId}/complete`, {
      time_spent_seconds: timeSpent,
      notes,
    });
    return data;
  },
};

// Videos API
export const videosAPI = {
  getBySectionId: async (sectionId) => {
    const { data } = await apiClient.get(`/videos/sections/${sectionId}`);
    return data;
  },
  
  scrapeForSection: async (sectionId, params = {}) => {
    const { data } = await apiClient.post(
      `/videos/sections/${sectionId}/scrape`,
      params
    );
    return data;
  },
};

// Practice API
export const practiceAPI = {
  getBySectionId: async (sectionId) => {
    const { data } = await apiClient.get(`/practice/sections/${sectionId}`);
    return data;
  },
  
  scrapeForSection: async (sectionId, params = {}) => {
    const { data} = await apiClient.post(
      `/practice/sections/${sectionId}/scrape`,
      params
    );
    return data;
  },
};
