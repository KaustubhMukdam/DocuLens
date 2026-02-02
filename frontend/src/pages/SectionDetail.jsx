import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useParams, useNavigate } from 'react-router-dom';
import { sectionsAPI, videosAPI, practiceAPI } from '@/api/sections';
import { bookmarksAPI } from '@/api/bookmarks';
import { aiAPI } from '@/api/ai';
import toast from 'react-hot-toast';
import Loading from '@/components/common/Loading.jsx';
import Button from '@/components/common/Button.jsx';
import { 
  Clock, CheckCircle, ArrowLeft, BookOpen, 
  Play, Code, ExternalLink, Youtube, Award,
  Lightbulb, ChevronDown, ChevronUp, Bookmark, 
  BookmarkCheck, Sparkles
} from 'lucide-react';

const SectionDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  
  // ALL STATE HOOKS AT THE TOP
  const [startTime] = useState(Date.now());
  const [notes, setNotes] = useState('');
  const [showVideos, setShowVideos] = useState(false);
  const [showProblems, setShowProblems] = useState(false);
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [aiSummary, setAiSummary] = useState(null);
  const [showAiSummary, setShowAiSummary] = useState(false);

  // ALL QUERY HOOKS
  const { data: section, isLoading } = useQuery({
    queryKey: ['section', id],
    queryFn: () => sectionsAPI.getById(id),
  });

  const { data: videos = [] } = useQuery({
    queryKey: ['videos', id],
    queryFn: () => videosAPI.getBySectionId(id),
    enabled: !!id,
  });

  const { data: problems = [] } = useQuery({
    queryKey: ['practice-problems', id],
    queryFn: () => practiceAPI.getBySectionId(id),
    enabled: !!id,
  });

  const { data: bookmarks } = useQuery({
    queryKey: ['bookmarks'],
    queryFn: bookmarksAPI.getMyBookmarks,
  });

  // ALL MUTATION HOOKS
  const scrapeVideosMutation = useMutation({
    mutationFn: (sectionId) => videosAPI.scrapeForSection(sectionId, { max_results: 3 }),
    onSuccess: () => {
      toast.success('Videos added successfully!');
      queryClient.invalidateQueries({ queryKey: ['videos', id] });
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to fetch videos');
    },
  });

  const scrapeProblemsMutation = useMutation({
    mutationFn: (sectionId) => practiceAPI.scrapeForSection(sectionId, { max_results: 5 }),
    onSuccess: () => {
      toast.success('Practice problems added!');
      queryClient.invalidateQueries({ queryKey: ['practice-problems', id] });
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to fetch problems');
    },
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

  const toggleBookmarkMutation = useMutation({
    mutationFn: async () => {
      if (isBookmarked) {
        return bookmarksAPI.deleteBookmark(id);
      } else {
        return bookmarksAPI.createBookmark(id, null);
      }
    },
    onSuccess: () => {
      setIsBookmarked(!isBookmarked);
      toast.success(isBookmarked ? 'Bookmark removed' : 'Bookmark added');
      queryClient.invalidateQueries({ queryKey: ['bookmarks'] });
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to update bookmark');
    },
  });

  const generateSummaryMutation = useMutation({
    mutationFn: async () => {
      return aiAPI.summarizeContent(
        section.content_raw,
        500,
        'concise'
      );
    },
    onSuccess: (data) => {
      setAiSummary(data.summary);
      setShowAiSummary(true);
      toast.success('AI summary generated!');
    },
    onError: (error) => {
      toast.error(error.response?.data?.error || 'Failed to generate summary');
    },
  });

  // ALL USEEFFECT HOOKS
  useEffect(() => {
    if (bookmarks && section) {
      const bookmarked = bookmarks.some(b => b.doc_section_id === section.id);
      setIsBookmarked(bookmarked);
    }
  }, [bookmarks, section]);

  // HELPER FUNCTIONS
  const handleMarkComplete = () => {
    const timeSpent = Math.floor((Date.now() - startTime) / 1000);
    markCompleteMutation.mutate({
      sectionId: id,
      timeSpent,
      notes,
    });
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty?.toLowerCase()) {
      case 'easy':
        return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400';
      case 'hard':
        return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  const formatDuration = (seconds) => {
    if (!seconds) return 'N/A';
    const minutes = Math.floor(seconds / 60);
    return `${minutes} min`;
  };

  // LOADING STATE
  if (isLoading) {
    return <Loading />;
  }

  // NOT FOUND STATE
  if (!section) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 dark:text-gray-400 text-lg">Section not found</p>
          <button
            onClick={() => navigate(-1)}
            className="mt-4 text-blue-600 dark:text-blue-400 hover:underline"
          >
            Go back
          </button>
        </div>
      </div>
    );
  }

  // MAIN RENDER
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-5xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <button
              onClick={() => navigate(-1)}
              className="flex items-center text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to sections
            </button>

            {/* Bookmark Button */}
            <button
              onClick={() => toggleBookmarkMutation.mutate()}
              disabled={toggleBookmarkMutation.isPending}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                isBookmarked
                  ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400 hover:bg-yellow-200 dark:hover:bg-yellow-900/50'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              {isBookmarked ? (
                <>
                  <BookmarkCheck className="w-5 h-5" />
                  Bookmarked
                </>
              ) : (
                <>
                  <Bookmark className="w-5 h-5" />
                  Bookmark
                </>
              )}
            </button>
          </div>

          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                {section.title}
              </h1>
              <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
                <span className="flex items-center">
                  <Clock className="w-4 h-4 mr-1" />
                  {section.estimated_time_minutes || 30} min
                </span>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(section.difficulty)}`}>
                  {section.difficulty || 'Medium'}
                </span>
                {section.is_completed && (
                  <span className="flex items-center text-green-600 dark:text-green-400">
                    <CheckCircle className="w-4 h-4 mr-1" />
                    Completed
                  </span>
                )}
              </div>
            </div>

            {section.source_url && (
              <a
                href={section.source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 flex items-center"
              >
                <ExternalLink className="w-4 h-4 mr-1" />
                Original Docs
              </a>
            )}
          </div>
        </div>

        {/* Content Summary */}
        {section.content_summary && (
          <div className="bg-blue-50 dark:bg-blue-900/30 border-l-4 border-blue-500 p-4 mb-6">
            <div className="flex items-start">
              <Lightbulb className="w-5 h-5 text-blue-500 dark:text-blue-400 mr-3 mt-1 flex-shrink-0" />
              <div>
                <h3 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">Quick Summary</h3>
                <p className="text-blue-800 dark:text-blue-200 whitespace-pre-wrap">{section.content_summary}</p>
              </div>
            </div>
          </div>
        )}

        {/* AI Summary Section */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center">
              <Sparkles className="w-6 h-6 mr-2 text-purple-600 dark:text-purple-400" />
              AI-Powered Summary
            </h2>
            
            {!showAiSummary && (
              <button
                onClick={() => generateSummaryMutation.mutate()}
                disabled={generateSummaryMutation.isPending}
                className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-medium rounded-lg transition-all disabled:opacity-50"
              >
                <Sparkles className="w-4 h-4" />
                {generateSummaryMutation.isPending ? 'Generating...' : 'Generate AI Summary'}
              </button>
            )}
          </div>

          {showAiSummary && aiSummary && (
            <div className="space-y-4">
              <div className="p-4 bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 rounded-lg border border-purple-200 dark:border-purple-800">
                <p className="text-gray-800 dark:text-gray-200 leading-relaxed whitespace-pre-wrap">
                  {aiSummary}
                </p>
              </div>
              
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400 flex items-center gap-1">
                  <Sparkles className="w-4 h-4" />
                  Powered by AI
                </span>
                <button
                  onClick={() => generateSummaryMutation.mutate()}
                  disabled={generateSummaryMutation.isPending}
                  className="text-purple-600 dark:text-purple-400 hover:text-purple-700 dark:hover:text-purple-300 font-medium"
                >
                  Regenerate
                </button>
              </div>
            </div>
          )}

          {!showAiSummary && !generateSummaryMutation.isPending && (
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Click the button above to generate an AI-powered summary of this section using advanced language models.
            </p>
          )}
        </div>

        {/* Main Content */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6 border border-gray-200 dark:border-gray-700">
          <div className="prose prose-lg dark:prose-invert max-w-none">
            <div className="whitespace-pre-wrap text-gray-800 dark:text-gray-200 leading-relaxed">
              {section.content_raw || 'Content is being processed...'}
            </div>
          </div>
        </div>

        {/* Video Resources Section */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6 border border-gray-200 dark:border-gray-700">
          <button
            onClick={() => setShowVideos(!showVideos)}
            className="w-full flex items-center justify-between mb-4"
          >
            <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center">
              <Youtube className="w-6 h-6 mr-2 text-red-600 dark:text-red-400" />
              Video Tutorials ({videos.length})
            </h2>
            {showVideos ? <ChevronUp className="text-gray-600 dark:text-gray-400" /> : <ChevronDown className="text-gray-600 dark:text-gray-400" />}
          </button>

          {showVideos && (
            <div>
              {videos.length === 0 ? (
                <div className="text-center py-8">
                  <p className="text-gray-600 dark:text-gray-400 mb-4">No video tutorials yet</p>
                  <Button
                    onClick={() => scrapeVideosMutation.mutate(id)}
                    disabled={scrapeVideosMutation.isPending}
                    variant="secondary"
                  >
                    {scrapeVideosMutation.isPending ? 'Finding Videos...' : '🎬 Find YouTube Tutorials'}
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  {videos.map((video) => (
                    <div key={video.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex gap-4">
                        {video.thumbnail_url && (
                          <img
                            src={video.thumbnail_url}
                            alt={video.title}
                            className="w-40 h-24 object-cover rounded"
                          />
                        )}
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-900 dark:text-white mb-1">{video.title}</h3>
                          {video.channel_name && (
                            <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">by {video.channel_name}</p>
                          )}
                          <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
                            {video.duration_seconds && (
                              <span className="flex items-center">
                                <Clock className="w-4 h-4 mr-1" />
                                {formatDuration(video.duration_seconds)}
                              </span>
                            )}
                            
                            <a
                              href={video.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 flex items-center"
                            >
                              <Play className="w-4 h-4 mr-1" />
                              Watch on YouTube
                            </a>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Practice Problems Section */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6 border border-gray-200 dark:border-gray-700">
          <button
            onClick={() => setShowProblems(!showProblems)}
            className="w-full flex items-center justify-between mb-4"
          >
            <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center">
              <Code className="w-6 h-6 mr-2 text-purple-600 dark:text-purple-400" />
              Practice Problems ({problems.length})
            </h2>
            {showProblems ? <ChevronUp className="text-gray-600 dark:text-gray-400" /> : <ChevronDown className="text-gray-600 dark:text-gray-400" />}
          </button>

          {showProblems && (
            <div>
              {problems.length === 0 ? (
                <div className="text-center py-8">
                  <p className="text-gray-600 dark:text-gray-400 mb-4">No practice problems yet</p>
                  <Button
                    onClick={() => scrapeProblemsMutation.mutate(id)}
                    disabled={scrapeProblemsMutation.isPending}
                    variant="secondary"
                  >
                    {scrapeProblemsMutation.isPending ? 'Finding Problems...' : '💪 Find LeetCode Problems'}
                  </Button>
                </div>
              ) : (
                <div className="space-y-3">
                  {problems.map((problem) => (
                    <div key={problem.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <h3 className="font-semibold text-gray-900 dark:text-white">{problem.title}</h3>
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(problem.difficulty)}`}>
                              {problem.difficulty}
                            </span>
                            <span className="text-xs text-gray-500 dark:text-gray-400 uppercase">{problem.platform}</span>
                          </div>
                          {problem.description && (
                            <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">{problem.description}</p>
                          )}
                          {problem.tags && problem.tags.length > 0 && (
                            <div className="flex flex-wrap gap-2">
                              {problem.tags.map((tag, idx) => (
                                <span key={idx} className="text-xs bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 px-2 py-1 rounded">
                                  {tag}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                        
                        <a
                          href={problem.problem_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="ml-4 text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 flex items-center text-sm whitespace-nowrap"
                        >
                          <ExternalLink className="w-4 h-4 mr-1" />
                          Solve
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Notes & Complete Section */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center">
            <BookOpen className="w-5 h-5 mr-2" />
            Your Notes
          </h2>
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Add your learning notes here..."
            className="w-full border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg p-3 mb-4 min-h-[120px] focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          
          <div className="flex gap-3">
            {!section.is_completed && (
              <Button
                onClick={handleMarkComplete}
                disabled={markCompleteMutation.isPending}
                className="flex-1"
              >
                <CheckCircle className="w-4 h-4 mr-2" />
                {markCompleteMutation.isPending ? 'Saving...' : 'Mark as Complete'}
              </Button>
            )}
            <Button
              onClick={() => navigate(-1)}
              variant="secondary"
              className="flex-1"
            >
              Continue Learning
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SectionDetail;