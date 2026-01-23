import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useParams, useNavigate } from 'react-router-dom';
import { sectionsAPI } from '@/api/sections';
import toast from 'react-hot-toast';
import Loading from '@/components/common/Loading';
import Button from '@/components/common/Button';
import { Clock, CheckCircle, ArrowLeft, BookOpen } from 'lucide-react';

const SectionDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [startTime] = useState(Date.now());
  const [notes, setNotes] = useState('');

  const { data: section, isLoading } = useQuery({
    queryKey: ['section', id],
    queryFn: () => sectionsAPI.getById(id),
  });

  const markCompleteMutation = useMutation({
    mutationFn: ({ sectionId, timeSpent, notes }) =>
      sectionsAPI.markComplete(sectionId, timeSpent, notes),
    onSuccess: () => {
      toast.success('Section marked as complete!');
      queryClient.invalidateQueries({ queryKey: ['progress-stats'] });
      queryClient.invalidateQueries({ queryKey: ['sections'] });
      navigate(-1);
    },
    onError: (error) => {
      toast.error(error.response?.data?.error || 'Failed to mark as complete');
    },
  });

  const handleMarkComplete = () => {
    const timeSpent = Math.floor((Date.now() - startTime) / 1000);
    markCompleteMutation.mutate({
      sectionId: id,
      timeSpent,
      notes,
    });
  };

  if (isLoading) {
    return <Loading fullScreen />;
  }

  if (!section) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Section Not Found
          </h2>
          <Button onClick={() => navigate(-1)}>Go Back</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container py-8">
        {/* Header */}
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6 transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to sections
        </button>

        <div className="bg-white rounded-lg shadow-md p-8 mb-8">
          {/* Title Section */}
          <div className="flex items-start gap-4 mb-6">
            <BookOpen className="w-8 h-8 text-primary-600 flex-shrink-0 mt-1" />
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-gray-900 mb-3">
                {section.title}
              </h1>
              
              <div className="flex items-center gap-6 text-sm text-gray-600">
                <span className="flex items-center gap-2">
                  <Clock className="w-4 h-4" />
                  {section.estimated_time_minutes || 30} minutes
                </span>
                <span className="px-3 py-1 rounded-full bg-gray-100 font-medium capitalize">
                  {section.difficulty || 'Medium'}
                </span>
                {section.is_quick_path && (
                  <span className="px-3 py-1 rounded-full bg-yellow-100 text-yellow-700 font-medium text-xs">
                    ⚡ Quick Path
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Content Section */}
          <div className="prose max-w-none mb-8">
            {section.content_summary && (
              <div className="mb-8">
                <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <span className="text-blue-600">📝</span>
                  AI Summary
                </h2>
                <div className="bg-blue-50 border-l-4 border-blue-500 p-6 rounded-r-lg">
                  <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
                    {section.content_summary}
                  </p>
                </div>
              </div>
            )}

            {section.content_raw && section.content_raw.length > 50 && (
              <div className="mb-8">
                <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <span className="text-green-600">📚</span>
                  Full Content
                </h2>
                <div className="bg-white border border-gray-200 p-6 rounded-lg">
                  <div className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                    {section.content_raw}
                  </div>
                </div>
              </div>
            )}

            {(!section.content_raw || section.content_raw.length < 50) && !section.content_summary && (
              <div className="text-center py-8 text-gray-500">
                <p>Content is being processed...</p>
              </div>
            )}

            {/* Source Link */}
            {section.source_url && (
              <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-2">Want to dive deeper?</p>
                <a
                  href={section.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium"
                >
                  <span>View Original Python Documentation</span>
                  <span>→</span>
                </a>
              </div>
            )}
          </div>

          {/* Mark Complete Section */}
          <div className="border-t pt-6">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-green-600" />
              Complete this section
            </h3>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Add your notes or key takeaways (optional)..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent mb-4 resize-none"
              rows={4}
            />
            <Button
              onClick={handleMarkComplete}
              isLoading={markCompleteMutation.isPending}
              className="flex items-center gap-2"
            >
              <CheckCircle className="w-5 h-5" />
              Mark as Complete
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SectionDetail;
