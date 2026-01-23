import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { progressAPI } from '@/api/progress';
import { languagesAPI } from '@/api/languages';
import { useAuthStore } from '@/store/authStore';
import Loading from '@/components/common/Loading';
import { Book, TrendingUp, Award, Flame } from 'lucide-react';
import Navbar from '@/components/layout/Navbar';

const Dashboard = () => {
  const user = useAuthStore((state) => state.user);

  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['progress-stats'],
    queryFn: progressAPI.getStats,
  });

  const { data: languages, isLoading: languagesLoading } = useQuery({
    queryKey: ['languages'],
    queryFn: () => languagesAPI.getAll(1, 6),
  });

  if (statsLoading || languagesLoading) {
    return <Loading fullScreen />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Welcome back, {user?.full_name || user?.username}!
        </h1>

        {/* Stats Grid */}
        <div className="grid md:grid-cols-4 gap-6 mb-12">
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-600">Sections Completed</h3>
              <Book className="w-5 h-5 text-primary-600" />
            </div>
            <p className="text-3xl font-bold text-gray-900">{stats?.sections_completed || 0}</p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-600">Learning Hours</h3>
              <TrendingUp className="w-5 h-5 text-green-600" />
            </div>
            <p className="text-3xl font-bold text-gray-900">{stats?.total_time_hours || 0}</p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-600">Current Streak</h3>
              <Flame className="w-5 h-5 text-orange-600" />
            </div>
            <p className="text-3xl font-bold text-gray-900">{stats?.current_streak_days || 0} days</p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-600">Languages Learning</h3>
              <Award className="w-5 h-5 text-purple-600" />
            </div>
            <p className="text-3xl font-bold text-gray-900">{stats?.languages_learning || 0}</p>
          </div>
        </div>

        {/* Languages Section */}
        <div>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Available Languages</h2>
            <Link to="/languages" className="text-primary-600 hover:text-primary-700 font-medium">
              View All →
            </Link>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {languages?.data?.map((lang) => (
              <Link
                key={lang.id}
                to={`/languages/${lang.slug}`}
                className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow"
              >
                <div className="flex items-center gap-4 mb-4">
                  {lang.logo_url && (
                    <img src={lang.logo_url} alt={lang.name} className="w-12 h-12 object-contain" />
                  )}
                  <div>
                    <h3 className="text-lg font-bold text-gray-900">{lang.name}</h3>
                    <p className="text-sm text-gray-500">{lang.version}</p>
                  </div>
                </div>
                <p className="text-sm text-gray-600 line-clamp-2">{lang.description}</p>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
