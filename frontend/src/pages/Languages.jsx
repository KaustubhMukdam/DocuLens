import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { languagesAPI } from '@/api/languages';
import Navbar from '@/components/layout/Navbar';
import Loading from '@/components/common/Loading';
import { ExternalLink } from 'lucide-react';

const Languages = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['languages'],
    queryFn: () => languagesAPI.getAll(1, 50),
  });

  if (isLoading) {
    return (
      <>
        <Navbar />
        <Loading fullScreen />
      </>
    );
  }

  return (
    <>
      <Navbar />
      <div className="min-h-screen bg-gray-50">
        <div className="container py-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">
            Programming Languages
          </h1>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {data?.data?.map((lang) => (
              <Link
                key={lang.id}
                to={`/languages/${lang.slug}`}
                className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow"
              >
                <div className="flex items-center gap-4 mb-4">
                  {lang.logo_url && (
                    <img 
                      src={lang.logo_url} 
                      alt={lang.name} 
                      className="w-16 h-16 object-contain"
                    />
                  )}
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-gray-900">{lang.name}</h3>
                    {lang.version && (
                      <p className="text-sm text-gray-500">Version {lang.version}</p>
                    )}
                  </div>
                </div>
                
                <p className="text-sm text-gray-600 mb-4 line-clamp-3">
                  {lang.description || 'No description available'}
                </p>

                {lang.official_doc_url && (
                  <div className="flex items-center text-xs text-primary-600 hover:text-primary-700">
                    <ExternalLink className="w-3 h-3 mr-1" />
                    Official Docs
                  </div>
                )}
              </Link>
            ))}
          </div>

          {(!data?.data || data.data.length === 0) && (
            <div className="text-center py-12">
              <p className="text-gray-500">No languages available yet.</p>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default Languages;
