import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useParams, Link } from 'react-router-dom';
import { languagesAPI } from '@/api/languages';
import Loading from '@/components/common/Loading';
import { Clock, BookOpen, Zap, Target } from 'lucide-react';

const LanguageDetail = () => {
  const { slug } = useParams();
  const [pathType, setPathType] = useState(null);

  const { data: language, isLoading: langLoading } = useQuery({
    queryKey: ['language', slug],
    queryFn: () => languagesAPI.getBySlug(slug),
  });

  const { data: sections, isLoading: sectionsLoading } = useQuery({
    queryKey: ['sections', slug, pathType],
    queryFn: () => languagesAPI.getSections(slug, pathType),
  });

  if (langLoading || sectionsLoading) {
    return <Loading fullScreen />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container py-8">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-8 mb-8">
          <div className="flex items-center gap-6 mb-6">
            {language?.logo_url && (
              <img 
                src={language.logo_url} 
                alt={language.name} 
                className="w-20 h-20 object-contain"
              />
            )}
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">
                {language?.name}
              </h1>
              {language?.version && (
                <p className="text-gray-600">Version {language.version}</p>
              )}
            </div>
          </div>

          <p className="text-gray-700 mb-6">{language?.description}</p>

          {/* Stats */}
          <div className="grid md:grid-cols-4 gap-4">
            <div className="flex items-center gap-3">
              <BookOpen className="w-5 h-5 text-primary-600" />
              <div>
                <p className="text-sm text-gray-600">Total Sections</p>
                <p className="text-lg font-bold">{language?.total_sections || 0}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Zap className="w-5 h-5 text-yellow-600" />
              <div>
                <p className="text-sm text-gray-600">Quick Path</p>
                <p className="text-lg font-bold">{language?.quick_path_sections || 0} sections</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Target className="w-5 h-5 text-green-600" />
              <div>
                <p className="text-sm text-gray-600">Deep Path</p>
                <p className="text-lg font-bold">{language?.deep_path_sections || 0} sections</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Clock className="w-5 h-5 text-blue-600" />
              <div>
                <p className="text-sm text-gray-600">Est. Time (Quick)</p>
                <p className="text-lg font-bold">
                  {language?.estimated_quick_time_hours || 0}h
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Path Type Filter */}
        <div className="flex gap-4 mb-6">
          <button
            onClick={() => setPathType(null)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              pathType === null
                ? 'bg-primary-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            All Sections
          </button>
          <button
            onClick={() => setPathType('quick')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              pathType === 'quick'
                ? 'bg-primary-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            Quick Path
          </button>
          <button
            onClick={() => setPathType('deep')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              pathType === 'deep'
                ? 'bg-primary-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            Deep Path
          </button>
        </div>

        {/* Sections List */}
        <div className="space-y-4">
          {sections?.map((section, index) => (
            <Link
              key={section.id}
              to={`/sections/${section.id}`}
              className="block bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="flex items-center justify-center w-8 h-8 rounded-full bg-primary-100 text-primary-600 font-bold text-sm">
                      {index + 1}
                    </span>
                    <h3 className="text-lg font-bold text-gray-900">
                      {section.title}
                    </h3>
                  </div>
                  
                  <div className="flex items-center gap-4 text-sm text-gray-600 ml-11">
                    <span className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      {section.estimated_time_minutes || 30} min
                    </span>
                    <span className="px-2 py-1 rounded bg-gray-100 text-xs font-medium">
                      {section.difficulty || 'Medium'}
                    </span>
                  </div>
                </div>

                {section.is_completed && (
                  <span className="px-3 py-1 bg-green-100 text-green-700 text-sm font-medium rounded-full">
                    ✓ Completed
                  </span>
                )}
              </div>
            </Link>
          ))}

          {(!sections || sections.length === 0) && (
            <div className="text-center py-12 bg-white rounded-lg">
              <p className="text-gray-500">No sections available for this path.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LanguageDetail;
