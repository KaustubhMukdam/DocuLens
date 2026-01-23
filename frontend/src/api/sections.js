import apiClient from './client';

export const sectionsAPI = {
  getById: async (sectionId) => {
    const response = await apiClient.get(`/docs/sections/${sectionId}`);
    return response.data;
  },

  markComplete: async (sectionId, timeSpent, notes = '') => {
    const response = await apiClient.post('/progress/mark-complete', {
      doc_section_id: sectionId,
      time_spent_seconds: timeSpent,
      notes,
    });
    return response.data;
  },
};
