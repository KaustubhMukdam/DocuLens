import apiClient from './client';

export const languagesAPI = {
  getAll: async (page = 1, pageSize = 20) => {
    const response = await apiClient.get('/languages', {
      params: { page, page_size: pageSize },
    });
    return response.data;
  },

  getBySlug: async (slug) => {
    const response = await apiClient.get(`/languages/${slug}`);
    return response.data;
  },

  // FIXED: Remove "languages" from the path - it should be /docs/{slug}/sections
  getSections: async (slug, pathType = null) => {
    const response = await apiClient.get(`/docs/${slug}/sections`, {
      params: pathType ? { path_type: pathType } : {},
    });
    return response.data;
  },
};
