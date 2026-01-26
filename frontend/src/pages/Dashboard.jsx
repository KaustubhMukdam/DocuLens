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
    return <Loading />;
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Message */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Welcome back, {user?.full_name || user?.username || 'User'}!
          </h1>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {/* Sections Completed */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 border border-gray-200 dark:border-gray-700 transition-colors">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
                Sections Completed
              </h3>
              <Book className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">
              {stats?.sections_completed || 0}
            </p>
          </div>

          {/* Learning Hours */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 border border-gray-200 dark:border-gray-700 transition-colors">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
                Learning Hours
              </h3>
              <TrendingUp className="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">
              {stats?.total_time_hours || 0}
            </p>
          </div>

          {/* Current Streak */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 border border-gray-200 dark:border-gray-700 transition-colors">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
                Current Streak
              </h3>
              <Flame className="w-6 h-6 text-orange-600 dark:text-orange-400" />
            </div>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">
              {stats?.current_streak_days || 0} days
            </p>
          </div>

          {/* Languages Learning */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 border border-gray-200 dark:border-gray-700 transition-colors">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
                Languages Learning
              </h3>
              <Award className="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">
              {stats?.languages_learning || 0}
            </p>
          </div>
        </div>

        {/* Available Languages */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              Available Languages
            </h2>
            <Link
              to="/languages"
              className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-medium transition-colors"
            >
              View All →
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {languages?.data?.map((lang) => (
              <Link
                key={lang.id}
                to={`/languages/${lang.slug}`}
                className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 border border-gray-200 dark:border-gray-700 hover:shadow-lg hover:border-blue-500 dark:hover:border-blue-400 transition-all"
              >
                <div className="flex items-center space-x-4 mb-4">
                  {/* FIXED: Use logo_url instead of icon */}
                  {lang.logo_url && (
                    <img
                      src={lang.logo_url}
                      alt={lang.name}
                      className="w-12 h-12 rounded-lg object-contain"
                    />
                  )}
                  <div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                      {lang.name}
                    </h3>
                    {lang.version && (
                      <span className="text-sm text-gray-500 dark:text-gray-400">
                        {lang.version}
                      </span>
                    )}
                  </div>
                </div>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  {lang.description}
                </p>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
