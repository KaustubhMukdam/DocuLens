import { Link } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { BookOpen, Zap, Target, ArrowRight } from 'lucide-react';

const Home = () => {
  const user = useAuthStore((state) => state.user);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Hero Section - Centered */}
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-center min-h-screen text-center py-20">
          {/* Main Heading */}
          <div className="max-w-4xl mx-auto mb-12">
            <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold text-gray-900 dark:text-white mb-6 leading-tight">
              Master Programming with{' '}
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                AI-Powered
              </span>{' '}
              Documentation
            </h1>
            
            <p className="text-lg sm:text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-10 max-w-3xl mx-auto">
              Learn faster with concise summaries, personalized roadmaps, and interactive learning paths from official documentation.
            </p>

            {/* CTA Button */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              {user ? (
                <Link
                  to="/dashboard"
                  className="group inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl hover:from-blue-700 hover:to-purple-700 transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl"
                >
                  Go to Dashboard
                  <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </Link>
              ) : (
                <>
                  <Link
                    to="/register"
                    className="group inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl hover:from-blue-700 hover:to-purple-700 transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl"
                  >
                    Get Started Free
                    <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                  </Link>
                  <Link
                    to="/login"
                    className="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-600 rounded-xl hover:border-blue-600 dark:hover:border-blue-400 transform hover:scale-105 transition-all duration-200 shadow-md hover:shadow-lg"
                  >
                    Sign In
                  </Link>
                </>
              )}
            </div>
          </div>

          {/* Feature Cards - Centered */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto mt-16 w-full">
            {/* Feature 1 */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-300 border border-gray-100 dark:border-gray-700">
              <div className="flex justify-center mb-6">
                <div className="p-4 bg-blue-100 dark:bg-blue-900/30 rounded-xl">
                  <BookOpen className="w-10 h-10 text-blue-600 dark:text-blue-400" />
                </div>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                Concise Summaries
              </h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                AI-powered summaries of official documentation, saving hours of reading time.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-300 border border-gray-100 dark:border-gray-700">
              <div className="flex justify-center mb-6">
                <div className="p-4 bg-purple-100 dark:bg-purple-900/30 rounded-xl">
                  <Zap className="w-10 h-10 text-purple-600 dark:text-purple-400" />
                </div>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                Quick & Deep Paths
              </h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                Choose between quick overviews or comprehensive deep dives based on your time.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-300 border border-gray-100 dark:border-gray-700">
              <div className="flex justify-center mb-6">
                <div className="p-4 bg-green-100 dark:bg-green-900/30 rounded-xl">
                  <Target className="w-10 h-10 text-green-600 dark:text-green-400" />
                </div>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                Track Progress
              </h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                Monitor your learning journey with streaks, achievements, and personalized insights.
              </p>
            </div>
          </div>

          {/* Footer Text */}
          <div className="mt-20 text-center">
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Start your journey to mastering programming documentation today
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;