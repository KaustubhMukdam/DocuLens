class ApiConstants {
  // Base URL
  static const String baseUrl = String.fromEnvironment(
    'BASE_URL',
    defaultValue: 'http://localhost:8000/api/v1',
  );

  // Timeout
  static const Duration connectTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);

  // Auth Endpoints
  static const String login = '/auth/login';
  static const String register = '/auth/register';
  static const String refresh = '/auth/refresh';
  static const String logout = '/auth/logout';
  static const String profile = '/users/me';

  // Language Endpoints
  static const String languages = '/languages';
  static String languageDetail(String slug) => '/languages/$slug';
  static String languageLearningPath(String slug) => '/languages/$slug/learning-path';

  // Section Endpoints
  static const String sections = '/sections';
  static String sectionDetail(String id) => '/sections/$id';

  // Progress Endpoints
  static const String markComplete = '/progress/mark-complete';
  static const String myProgress = '/progress/me';
  static const String progressStats = '/progress/stats';

  // Learning Path Endpoints
  static const String learningPaths = '/learning-paths';
  static const String myLearningPaths = '/learning-paths/me';
}
