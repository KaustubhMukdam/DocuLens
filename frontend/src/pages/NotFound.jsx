import { Link } from 'react-router-dom';
import { Home, ArrowLeft } from 'lucide-react';
import Navbar from '@/components/layout/Navbar';

const NotFound = () => {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar />
      
      <div className="flex flex-col items-center justify-center px-4 py-20">
        <div className="text-center">
          {/* 404 Number */}
          <h1 className="text-9xl font-bold text-blue-600 dark:text-blue-400">
            404
          </h1>
          
          {/* Message */}
          <h2 className="mt-4 text-3xl font-semibold text-gray-900 dark:text-white">
            Page Not Found
          </h2>
          
          <p className="mt-4 text-lg text-gray-600 dark:text-gray-400 max-w-md">
            Sorry, we couldn't find the page you're looking for. 
            It might have been moved or deleted.
          </p>
          
          {/* Actions */}
          <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/"
              className="inline-flex items-center px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
            >
              <Home className="w-5 h-5 mr-2" />
              Go Home
            </Link>
            
            <button
              onClick={() => window.history.back()}
              className="inline-flex items-center px-6 py-3 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-900 dark:text-white font-medium rounded-lg transition-colors"
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              Go Back
            </button>
          </div>
          
          {/* Illustration or Additional Links */}
          <div className="mt-12">
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Need help?{' '}
              <Link to="/contact" className="text-blue-600 dark:text-blue-400 hover:underline">
                Contact Support
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
