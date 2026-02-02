import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, X, Book, FileText, Loader2 } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';

const SearchBar = () => {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [debouncedQuery, setDebouncedQuery] = useState('');
  const navigate = useNavigate();
  const searchRef = useRef(null);

  // Debounce search query
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(query);
    }, 300);

    return () => clearTimeout(timer);
  }, [query]);

  // Search API call
  const { data: results, isLoading } = useQuery({
    queryKey: ['search', debouncedQuery],
    queryFn: async () => {
      if (debouncedQuery.length < 2) return null;
      
      const response = await fetch(
        `http://localhost:8000/api/v1/docs/search?q=${encodeURIComponent(debouncedQuery)}`,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        }
      );
      return response.json();
    },
    enabled: debouncedQuery.length >= 2,
  });

  // Close on click outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleResultClick = (type, slug, id) => {
    if (type === 'language') {
      navigate(`/languages/${slug}`);
    } else {
      navigate(`/sections/${id}`);
    }
    setQuery('');
    setIsOpen(false);
  };

  return (
    <div ref={searchRef} className="relative w-full max-w-md">
      {/* Search Input */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          placeholder="Search languages, sections..."
          className="w-full pl-10 pr-10 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
        />
        {query && (
          <button
            onClick={() => {
              setQuery('');
              setIsOpen(false);
            }}
            className="absolute right-3 top-1/2 transform -translate-y-1/2"
          >
            <X className="w-5 h-5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300" />
          </button>
        )}
      </div>

      {/* Search Results Dropdown */}
      {isOpen && query.length >= 2 && (
        <div className="absolute top-full mt-2 w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg max-h-96 overflow-y-auto z-50">
          {isLoading ? (
            <div className="p-4 text-center">
              <Loader2 className="w-6 h-6 animate-spin mx-auto text-blue-600 dark:text-blue-400" />
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">Searching...</p>
            </div>
          ) : results && results.total_results > 0 ? (
            <div className="p-2">
              {/* Languages */}
              {results.languages.length > 0 && (
                <div className="mb-4">
                  <div className="px-3 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">
                    Languages
                  </div>
                  {results.languages.map((lang) => (
                    <button
                      key={lang.id}
                      onClick={() => handleResultClick('language', lang.slug)}
                      className="w-full px-3 py-2 text-left hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                    >
                      <div className="flex items-center gap-3">
                        {lang.logo_url && (
                          <img src={lang.logo_url} alt={lang.name} className="w-8 h-8 rounded" />
                        )}
                        <div>
                          <div className="flex items-center gap-2">
                            <Book className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                            <span className="font-medium text-gray-900 dark:text-white">
                              {lang.name}
                            </span>
                          </div>
                          <p className="text-xs text-gray-600 dark:text-gray-400 line-clamp-1">
                            {lang.description}
                          </p>
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              )}

              {/* Sections */}
              {results.sections.length > 0 && (
                <div>
                  <div className="px-3 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">
                    Sections
                  </div>
                  {results.sections.map((section) => (
                    <button
                      key={section.id}
                      onClick={() => handleResultClick('section', section.language_slug, section.id)}
                      className="w-full px-3 py-2 text-left hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                    >
                      <div className="flex items-start gap-2">
                        <FileText className="w-4 h-4 text-green-600 dark:text-green-400 mt-1 flex-shrink-0" />
                        <div className="flex-1 min-w-0">
                          <div className="font-medium text-gray-900 dark:text-white">
                            {section.title}
                          </div>
                          <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400 mt-1">
                            <span>{section.language_name}</span>
                            <span>•</span>
                            <span className="capitalize">{section.difficulty}</span>
                          </div>
                          <p className="text-xs text-gray-600 dark:text-gray-400 mt-1 line-clamp-2">
                            {section.content_preview}...
                          </p>
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>
          ) : query.length >= 2 ? (
            <div className="p-4 text-center text-gray-600 dark:text-gray-400">
              <Search className="w-8 h-8 mx-auto mb-2 text-gray-400" />
              <p className="text-sm">No results found for "{query}"</p>
            </div>
          ) : null}
        </div>
      )}
    </div>
  );
};

export default SearchBar;