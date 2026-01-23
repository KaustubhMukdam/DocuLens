import { Link } from 'react-router-dom';
import { Book, Zap, Target, ArrowRight } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';
import Button from '@/components/common/Button';

const Home = () => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white">
      {/* Hero Section */}
      <div className="container py-20">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Master Programming with{' '}
            <span className="text-primary-600">AI-Powered</span> Documentation
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Learn faster with concise summaries, personalized roadmaps, and interactive learning paths
            from official documentation.
          </p>
          <div className="flex gap-4 justify-center">
            {isAuthenticated ? (
              <Link to="/dashboard">
                <Button size="lg">
                  Go to Dashboard <ArrowRight className="ml-2 w-5 h-5" />
                </Button>
              </Link>
            ) : (
              <>
                <Link to="/register">
                  <Button size="lg">Get Started Free</Button>
                </Link>
                <Link to="/login">
                  <Button variant="outline" size="lg">
                    Sign In
                  </Button>
                </Link>
              </>
            )}
          </div>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-8 mt-20">
          <div className="bg-white p-8 rounded-xl shadow-lg">
            <Book className="w-12 h-12 text-primary-600 mb-4" />
            <h3 className="text-xl font-bold mb-2">Concise Summaries</h3>
            <p className="text-gray-600">
              AI-powered summaries of official documentation, saving hours of reading time.
            </p>
          </div>
          <div className="bg-white p-8 rounded-xl shadow-lg">
            <Zap className="w-12 h-12 text-primary-600 mb-4" />
            <h3 className="text-xl font-bold mb-2">Quick & Deep Paths</h3>
            <p className="text-gray-600">
              Choose between quick overviews or comprehensive deep dives based on your time.
            </p>
          </div>
          <div className="bg-white p-8 rounded-xl shadow-lg">
            <Target className="w-12 h-12 text-primary-600 mb-4" />
            <h3 className="text-xl font-bold mb-2">Track Progress</h3>
            <p className="text-gray-600">
              Monitor your learning journey with streaks, achievements, and personalized insights.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
