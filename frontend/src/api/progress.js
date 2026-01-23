import apiClient from './client';

export const progressAPI = {
  getMyProgress: async (languageId = null) => {
    const response = await apiClient.get('/progress/me', {
      params: languageId ? { language_id: languageId } : {},
    });
    return response.data;
  },

  getStats: async () => {
    const response = await apiClient.get('/progress/stats');
    return response.data;
  },
};
