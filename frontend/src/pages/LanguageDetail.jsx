import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useParams, Link } from 'react-router-dom';
import { languagesAPI } from '@/api/languages';
import Loading from '@/components/common/Loading';
import Navbar from '@/components/layout/Navbar';
import { Clock, BookOpen, Zap, Target } from 'lucide-react';

const LanguageDetail = () => {
  const { slug } = useParams();
  const [pathType, setPathType] = useState(null);

  const { data: language, isLoading: langLoading } = useQuery({
    queryKey: ['language', slug],
    queryFn: () => languagesAPI.getBySlug(slug),
  });

  const { data: sections, isLoading: sectionsLoading, error: sectionsError } = useQuery({
    queryKey: ['sections', slug, pathType],
    queryFn: () => languagesAPI.getSections(slug, pathType),
    enabled: !!language,
  });

  // Log for debugging
  console.log('Sections data:', sections);
  console.log('Sections error:', sectionsError);

  if (langLoading) {
    return <Loading />;
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Language Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-4 mb-4">
            {language?.logo_url && (
              <img
                src={language.logo_url}
                alt={language.name}
                className="w-20 h-20 rounded-xl object-contain"
              />
            )}
            <div>
              <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
                {language?.name}
              </h1>
              {language?.version && (
                <span className="text-lg text-gray-600 dark:text-gray-400">
                  Version {language.version}
                </span>
              )}
            </div>
          </div>
          <p className="text-gray-600 dark:text-gray-400 text-lg">
            {language?.description}
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700 transition-colors">
            <div className="flex items-center space-x-2 mb-2">
              <BookOpen className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
                Total Sections
              </h3>
            </div>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">
              {language?.total_sections || 0}
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700 transition-colors">
            <div className="flex items-center space-x-2 mb-2">
              <Zap className="w-5 h-5 text-yellow-600 dark:text-yellow-400" />
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
                Quick Path
              </h3>
            </div>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">
              {language?.quick_path_sections || 0} sections
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700 transition-colors">
            <div className="flex items-center space-x-2 mb-2">
              <Target className="w-5 h-5 text-green-600 dark:text-green-400" />
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
                Deep Path
              </h3>
            </div>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">
              {language?.deep_path_sections || 0} sections
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700 transition-colors">
            <div className="flex items-center space-x-2 mb-2">
              <Clock className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
                Est. Time (Quick)
              </h3>
            </div>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">
              {language?.estimated_quick_time_hours || 0}h
            </p>
          </div>
        </div>

        {/* Path Filter Tabs */}
        <div className="flex space-x-2 mb-6 border-b border-gray-200 dark:border-gray-700">
          <button
            onClick={() => setPathType(null)}
            className={`px-6 py-3 font-medium transition-colors ${
              pathType === null
                ? 'text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
            }`}
          >
            All Sections
          </button>
          <button
            onClick={() => setPathType('quick')}
            className={`px-6 py-3 font-medium transition-colors ${
              pathType === 'quick'
                ? 'text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
            }`}
          >
            Quick Path
          </button>
          <button
            onClick={() => setPathType('deep')}
            className={`px-6 py-3 font-medium transition-colors ${
              pathType === 'deep'
                ? 'text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
            }`}
          >
            Deep Path
          </button>
        </div>

        {/* Sections List */}
        {sectionsLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-blue-600 dark:border-blue-400 mx-auto"></div>
          </div>
        ) : sectionsError ? (
          <div className="text-center py-12 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800">
            <p className="text-red-600 dark:text-red-400 text-lg">
              Error loading sections: {sectionsError.message}
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {sections && sections.length > 0 ? (
              sections.map((section, index) => (
                <Link
                  key={section.id}
                  to={`/sections/${section.id}`}
                  className="block bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700 hover:shadow-lg hover:border-blue-500 dark:hover:border-blue-400 transition-all"
                >
                  <div className="flex items-center space-x-4">
                    <div className="flex-shrink-0 w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center">
                      <span className="text-xl font-bold text-blue-600 dark:text-blue-400">
                        {index + 1}
                      </span>
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-1">
                        {section.title}
                      </h3>
                      <div className="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400">
                        <span className="flex items-center">
                          <Clock className="w-4 h-4 mr-1" />
                          {section.estimated_time_minutes} min
                        </span>
                        <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded text-gray-700 dark:text-gray-300 capitalize">
                          {section.difficulty}
                        </span>
                      </div>
                    </div>
                  </div>
                </Link>
              ))
            ) : (
              <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
                <p className="text-gray-600 dark:text-gray-400 text-lg">
                  No sections available for this path.
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default LanguageDetail;
