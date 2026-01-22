class AppConstants {
  // App Info
  static const String appName = 'DocuLens';
  static const String appTagline = 'Learn from Official Docs';
  static const String appVersion = '1.0.0';

  // Storage Keys
  static const String accessTokenKey = 'access_token';
  static const String refreshTokenKey = 'refresh_token';
  static const String userIdKey = 'user_id';
  static const String themeKey = 'theme_mode';
  static const String onboardingKey = 'onboarding_completed';

  // Pagination
  static const int defaultPageSize = 20;
  static const int maxPageSize = 100;

  // Animation Durations
  static const Duration shortAnimation = Duration(milliseconds: 200);
  static const Duration mediumAnimation = Duration(milliseconds: 300);
  static const Duration longAnimation = Duration(milliseconds: 500);

  // Spacing
  static const double spacing4 = 4.0;
  static const double spacing8 = 8.0;
  static const double spacing12 = 12.0;
  static const double spacing16 = 16.0;
  static const double spacing20 = 20.0;
  static const double spacing24 = 24.0;
  static const double spacing32 = 32.0;
  static const double spacing48 = 48.0;

  // Border Radius
  static const double radiusSmall = 8.0;
  static const double radiusMedium = 12.0;
  static const double radiusLarge = 16.0;
  static const double radiusXLarge = 24.0;

  // Onboarding
  static const List<OnboardingData> onboardingSlides = [
    OnboardingData(
      title: 'Learn from\nOfficial Docs',
      description: 'Master programming by learning directly from official documentation, structured and simplified.',
      image: '📚',
    ),
    OnboardingData(
      title: 'AI-Powered\nSummaries',
      description: 'Get concise, AI-generated summaries of complex documentation with code examples.',
      image: '🧠',
    ),
    OnboardingData(
      title: 'Track Your\nProgress',
      description: 'Stay motivated with streaks, achievements, and personalized learning paths.',
      image: '🎯',
    ),
  ];
}

class OnboardingData {
  final String title;
  final String description;
  final String image;

  const OnboardingData({
    required this.title,
    required this.description,
    required this.image,
  });
}
