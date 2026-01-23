import apiClient from './client';

export const aiAPI = {
  summarizeContent: async (content, maxLength = 500, style = 'concise') => {
    const response = await apiClient.post('/ai/summarize', {
      content,
      max_length: maxLength,
      style,
    });
    return response.data;
  },

  generateRoadmap: async (data) => {
    const response = await apiClient.post('/ai/generate-roadmap', data);
    return response.data;
  },
};
