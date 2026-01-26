import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useParams, useNavigate } from 'react-router-dom';
import { sectionsAPI, videosAPI, practiceAPI } from '@/api/sections';
import toast from 'react-hot-toast';
import Loading from '@/components/common/Loading';
import Button from '@/components/common/Button';
import { 
  Clock, CheckCircle, ArrowLeft, BookOpen, 
  Play, Code, ExternalLink, Youtube, Award,
  Lightbulb, ChevronDown, ChevronUp
} from 'lucide-react';

const SectionDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [startTime] = useState(Date.now());
  const [notes, setNotes] = useState('');
  const [showVideos, setShowVideos] = useState(false);
  const [showProblems, setShowProblems] = useState(false);

  // Fetch section data
  const { data: section, isLoading } = useQuery({
    queryKey: ['section', id],
    queryFn: () => sectionsAPI.getById(id),
  });

  // Fetch videos for this section
  const { data: videos = [] } = useQuery({
    queryKey: ['videos', id],
    queryFn: () => videosAPI.getBySectionId(id),
    enabled: !!id,
  });

  // Fetch practice problems for this section
  const { data: problems = [] } = useQuery({
    queryKey: ['practice-problems', id],
    queryFn: () => practiceAPI.getBySectionId(id),
    enabled: !!id,
  });

  // Auto-scrape videos mutation
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

  // Auto-scrape problems mutation
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

  // Mark complete mutation
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
    return <Loading />;
  }

  if (!section) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">Section not found</p>
      </div>
    );
  }

  const getDifficultyColor = (difficulty) => {
    switch (difficulty?.toLowerCase()) {
      case 'easy':
        return 'bg-green-100 text-green-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'hard':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatDuration = (seconds) => {
    if (!seconds) return 'N/A';
    const minutes = Math.floor(seconds / 60);
    return `${minutes} min`;
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center text-blue-600 hover:text-blue-700 mb-4"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to sections
        </button>

        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              {section.title}
            </h1>
            <div className="flex items-center gap-4 text-sm text-gray-600">
              <span className="flex items-center">
                <Clock className="w-4 h-4 mr-1" />
                {section.estimated_time_minutes || 30} min
              </span>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(section.difficulty)}`}>
                {section.difficulty || 'Medium'}
              </span>
              {section.is_completed && (
                <span className="flex items-center text-green-600">
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
              className="text-blue-600 hover:text-blue-700 flex items-center"
            >
              <ExternalLink className="w-4 h-4 mr-1" />
              Original Docs
            </a>
          )}
        </div>
      </div>

      {/* Content Summary */}
      {section.content_summary && (
        <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6">
          <div className="flex items-start">
            <Lightbulb className="w-5 h-5 text-blue-500 mr-3 mt-1 flex-shrink-0" />
            <div>
              <h3 className="font-semibold text-blue-900 mb-2">Quick Summary</h3>
              <p className="text-blue-800 whitespace-pre-wrap">{section.content_summary}</p>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="prose max-w-none">
          <div className="whitespace-pre-wrap text-gray-800 leading-relaxed">
            {section.content_raw || 'Content is being processed...'}
          </div>
        </div>
      </div>

      {/* Video Resources Section */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <button
          onClick={() => setShowVideos(!showVideos)}
          className="w-full flex items-center justify-between mb-4"
        >
          <h2 className="text-xl font-bold text-gray-900 flex items-center">
            <Youtube className="w-6 h-6 mr-2 text-red-600" />
            Video Tutorials ({videos.length})
          </h2>
          {showVideos ? <ChevronUp /> : <ChevronDown />}
        </button>

        {showVideos && (
          <div>
            {videos.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-gray-600 mb-4">No video tutorials yet</p>
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
                  <div key={video.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex gap-4">
                      {video.thumbnail_url && (
                        <img
                          src={video.thumbnail_url}
                          alt={video.title}
                          className="w-40 h-24 object-cover rounded"
                        />
                      )}
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900 mb-1">{video.title}</h3>
                        {video.channel_name && (
                          <p className="text-sm text-gray-600 mb-2">by {video.channel_name}</p>
                        )}
                        <div className="flex items-center gap-4 text-sm text-gray-500">
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
                            className="text-blue-600 hover:text-blue-700 flex items-center"
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
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <button
          onClick={() => setShowProblems(!showProblems)}
          className="w-full flex items-center justify-between mb-4"
        >
          <h2 className="text-xl font-bold text-gray-900 flex items-center">
            <Code className="w-6 h-6 mr-2 text-purple-600" />
            Practice Problems ({problems.length})
          </h2>
          {showProblems ? <ChevronUp /> : <ChevronDown />}
        </button>

        {showProblems && (
          <div>
            {problems.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-gray-600 mb-4">No practice problems yet</p>
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
                  <div key={problem.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="font-semibold text-gray-900">{problem.title}</h3>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(problem.difficulty)}`}>
                            {problem.difficulty}
                          </span>
                          <span className="text-xs text-gray-500 uppercase">{problem.platform}</span>
                        </div>
                        {problem.description && (
                          <p className="text-sm text-gray-600 mb-2">{problem.description}</p>
                        )}
                        {problem.tags && problem.tags.length > 0 && (
                          <div className="flex flex-wrap gap-2">
                            {problem.tags.map((tag, idx) => (
                              <span key={idx} className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
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
                        className="ml-4 text-blue-600 hover:text-blue-700 flex items-center text-sm whitespace-nowrap"
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
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <BookOpen className="w-5 h-5 mr-2" />
          Your Notes
        </h2>
        <textarea
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          placeholder="Add your learning notes here..."
          className="w-full border rounded-lg p-3 mb-4 min-h-[120px] focus:ring-2 focus:ring-blue-500 focus:border-transparent"
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
  );
};

export default SectionDetail;
