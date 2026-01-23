import { Link } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { Home, Book, User, LogOut, BarChart } from 'lucide-react';

const Navbar = () => {
  const { user, isAuthenticated, logout } = useAuthStore();

  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="container">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-primary-700 rounded-lg flex items-center justify-center">
              <Book className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">DocuLens</span>
          </Link>

          {/* Navigation Links */}
          {isAuthenticated ? (
            <div className="flex items-center gap-6">
              <Link
                to="/dashboard"
                className="flex items-center gap-2 text-gray-700 hover:text-primary-600 transition-colors"
              >
                <BarChart className="w-5 h-5" />
                <span className="font-medium">Dashboard</span>
              </Link>
              
              <Link
                to="/languages"
                className="flex items-center gap-2 text-gray-700 hover:text-primary-600 transition-colors"
              >
                <Book className="w-5 h-5" />
                <span className="font-medium">Languages</span>
              </Link>

              <div className="flex items-center gap-3 pl-6 border-l border-gray-200">
                <Link
                  to="/profile"
                  className="flex items-center gap-2 text-gray-700 hover:text-primary-600 transition-colors"
                >
                  <div className="w-8 h-8 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center font-bold">
                    {user?.username?.charAt(0).toUpperCase()}
                  </div>
                  <span className="font-medium">{user?.username}</span>
                </Link>

                <button
                  onClick={logout}
                  className="p-2 text-gray-500 hover:text-red-600 transition-colors"
                  title="Logout"
                >
                  <LogOut className="w-5 h-5" />
                </button>
              </div>
            </div>
          ) : (
            <div className="flex items-center gap-4">
              <Link
                to="/login"
                className="text-gray-700 hover:text-primary-600 font-medium transition-colors"
              >
                Sign In
              </Link>
              <Link
                to="/register"
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
              >
                Get Started
              </Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
