import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { bookmarksAPI } from '@/api/bookmarks';
import Navbar from '@/components/layout/Navbar.jsx';
import Loading from '@/components/common/Loading.jsx';
import toast from 'react-hot-toast';
import { 
  Bookmark, Trash2, Clock, Book, 
  Calendar, BookOpen 
} from 'lucide-react';

const Bookmarks = () => {
  const queryClient = useQueryClient();

  const { data: bookmarks, isLoading } = useQuery({
    queryKey: ['bookmarks'],
    queryFn: bookmarksAPI.getMyBookmarks,
  });

  const deleteBookmarkMutation = useMutation({
    mutationFn: (sectionId) => bookmarksAPI.deleteBookmark(sectionId),
    onSuccess: () => {
      toast.success('Bookmark removed');
      queryClient.invalidateQueries({ queryKey: ['bookmarks'] });
    },
    onError: () => {
      toast.error('Failed to remove bookmark');
    },
  });

  if (isLoading) {
    return (
      <>
        <Navbar />
        <Loading />
      </>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
            <Bookmark className="w-8 h-8 text-yellow-600 dark:text-yellow-400" />
            My Bookmarks
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            {bookmarks?.length || 0} saved sections
          </p>
        </div>

        {/* Bookmarks List */}
        {bookmarks && bookmarks.length > 0 ? (
          <div className="space-y-4">
            {bookmarks.map((bookmark) => (
              <div
                key={bookmark.id}
                className="bg-white dark:bg-gray-800 rounded-xl shadow-md border border-gray-200 dark:border-gray-700 p-6 hover:shadow-lg transition-all"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <Link
                      to={`/sections/${bookmark.doc_section_id}`}
                      className="group"
                    >
                      <h3 className="text-xl font-bold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors mb-2">
                        {bookmark.section_title}
                      </h3>
                    </Link>

                    <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600 dark:text-gray-400 mb-3">
                      <span className="flex items-center gap-1">
                        <Book className="w-4 h-4" />
                        {bookmark.language_name}
                      </span>
                      <span className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        Saved {new Date(bookmark.created_at).toLocaleDateString()}
                      </span>
                    </div>

                    {bookmark.notes && (
                      <div className="mt-3 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border-l-4 border-blue-500">
                        <p className="text-sm text-gray-700 dark:text-gray-300">
                          <strong>Notes:</strong> {bookmark.notes}
                        </p>
                      </div>
                    )}
                  </div>

                  <button
                    onClick={() => deleteBookmarkMutation.mutate(bookmark.doc_section_id)}
                    disabled={deleteBookmarkMutation.isPending}
                    className="ml-4 p-2 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-lg transition-colors"
                    title="Remove bookmark"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>

                <div className="mt-4">
                  <Link
                    to={`/sections/${bookmark.doc_section_id}`}
                    className="inline-flex items-center text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-medium text-sm"
                  >
                    <BookOpen className="w-4 h-4 mr-1" />
                    Continue reading →
                  </Link>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <Bookmark className="w-16 h-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              No bookmarks yet
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Save sections you want to revisit later
            </p>
            <Link
              to="/languages"
              className="inline-flex items-center px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
            >
              <Book className="w-5 h-5 mr-2" />
              Browse Languages
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default Bookmarks;