import apiClient from './client';

export const bookmarksAPI = {
  // Get all user bookmarks
  getMyBookmarks: async (languageId = null) => {
    const response = await apiClient.get('/bookmarks', {
      params: languageId ? { language_id: languageId } : {},
    });
    return response.data;
  },

  // Create bookmark
  createBookmark: async (sectionId, notes = null) => {
    const response = await apiClient.post('/bookmarks', {
      doc_section_id: sectionId,
      notes,
    });
    return response.data;
  },

  // Delete bookmark by section ID
  deleteBookmark: async (sectionId) => {
    const response = await apiClient.delete(`/bookmarks/section/${sectionId}`);
    return response.data;
  },

  // Update bookmark notes
  updateBookmark: async (bookmarkId, notes) => {
    const response = await apiClient.put(`/bookmarks/${bookmarkId}`, {
      notes,
    });
    return response.data;
  },
};