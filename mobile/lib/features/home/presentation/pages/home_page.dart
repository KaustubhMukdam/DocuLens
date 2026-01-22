import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';
import '../../../../core/theme/app_theme.dart';
import '../../../../core/network/api_client.dart';
import '../../../../shared/widgets/loading_indicator.dart';
import '../widgets/language_card.dart';
import '../widgets/stats_card.dart';
import '../widgets/streak_indicator.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  bool _isLoading = false;

  // Mock data - will be replaced with real API calls
  final List<Map<String, dynamic>> _languages = [
    {
      'id': '400c02cc-7d1f-48b5-87a9-19700aa29c96',
      'name': 'Python',
      'slug': 'python',
      'icon': '🐍',
      'totalSections': 30,
      'completedSections': 12,
      'estimatedHours': 23,
      'color': Color(0xFF3776AB),
    },
    {
      'id': '2',
      'name': 'JavaScript',
      'slug': 'javascript',
      'icon': '⚡',
      'totalSections': 25,
      'completedSections': 0,
      'estimatedHours': 18,
      'color': Color(0xFFF7DF1E),
      'isLocked': true,
    },
    {
      'id': '3',
      'name': 'Java',
      'slug': 'java',
      'icon': '☕',
      'totalSections': 28,
      'completedSections': 0,
      'estimatedHours': 20,
      'color': Color(0xFFE76F00),
      'isLocked': true,
    },
  ];

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() => _isLoading = true);
    try {
      // Fetch real languages from API
      final response = await ApiClient().getLanguages();
      if (response.statusCode == 200) {
        // TODO: Update _languages list with real data
        // setState(() => _languages = response.data);
      }
    } catch (e) {
      // Handle error silently for now
      print('Error loading languages: $e');
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      body: SafeArea(
        child: _isLoading
            ? const LoadingIndicator(message: 'Loading your dashboard...')
            : CustomScrollView(
                slivers: [
                  // App Bar
                  SliverAppBar(
                    floating: true,
                    snap: true,
                    backgroundColor: isDark ? AppTheme.darkBackground : AppTheme.lightBackground,
                    title: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'DocuLens',
                          style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                                fontWeight: FontWeight.w700,
                              ),
                        ),
                        Text(
                          'Learn from Official Docs',
                          style: Theme.of(context).textTheme.bodySmall?.copyWith(
                                color: isDark ? AppTheme.darkTextSecondary : AppTheme.lightTextSecondary,
                              ),
                        ),
                      ],
                    ),
                    actions: [
                      // Theme Toggle
                      IconButton(
                        icon: Icon(
                          isDark ? Icons.light_mode_rounded : Icons.dark_mode_rounded,
                        ),
                        onPressed: () {
                          // TODO: Implement theme toggle
                        },
                      ),
                      // Profile
                      IconButton(
                        icon: const Icon(Icons.person_rounded),
                        onPressed: () => context.go('/profile'),
                      ),
                    ],
                  ),

                  // Streak Indicator
                  SliverToBoxAdapter(
                    child: Padding(
                      padding: const EdgeInsets.all(20),
                      child: const StreakIndicator(
                        currentStreak: 5,
                        longestStreak: 12,
                      ).animate().fadeIn(delay: 100.ms, duration: 400.ms).slideX(begin: -0.2, end: 0),
                    ),
                  ),

                  // Stats Cards
                  SliverToBoxAdapter(
                    child: Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 20),
                      child: Row(
                        children: [
                          Expanded(
                            child: StatsCard(
                              icon: Icons.check_circle_outline_rounded,
                              value: '12',
                              label: 'Completed',
                              color: isDark ? AppTheme.darkSuccess : AppTheme.lightSuccess,
                            ).animate().fadeIn(delay: 200.ms, duration: 400.ms).scale(begin: const Offset(0.8, 0.8)),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: StatsCard(
                              icon: Icons.schedule_rounded,
                              value: '23h',
                              label: 'Learning Time',
                              color: isDark ? AppTheme.darkPrimary : AppTheme.lightPrimary,
                            ).animate().fadeIn(delay: 300.ms, duration: 400.ms).scale(begin: const Offset(0.8, 0.8)),
                          ),
                        ],
                      ),
                    ),
                  ),

                  // Section Title
                  SliverToBoxAdapter(
                    child: Padding(
                      padding: const EdgeInsets.fromLTRB(20, 32, 20, 16),
                      child: Text(
                        'Choose Your Language',
                        style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                              fontWeight: FontWeight.w700,
                            ),
                      ).animate().fadeIn(delay: 400.ms, duration: 400.ms).slideX(begin: -0.2, end: 0),
                    ),
                  ),

                  // Languages List
                  SliverPadding(
                    padding: const EdgeInsets.fromLTRB(20, 0, 20, 32),
                    sliver: SliverList(
                      delegate: SliverChildBuilderDelegate(
                        (context, index) {
                          final language = _languages[index];
                          return Padding(
                            padding: const EdgeInsets.only(bottom: 16),
                            child: LanguageCard(
                              name: language['name'],
                              icon: language['icon'],
                              totalSections: language['totalSections'],
                              completedSections: language['completedSections'],
                              estimatedHours: language['estimatedHours'],
                              color: language['color'],
                              isLocked: language['isLocked'] ?? false,
                              onTap: () {
                                if (language['isLocked'] != true) {
                                  context.go('/language/${language['slug']}');
                                }
                              },
                            )
                                .animate()
                                .fadeIn(delay: (500 + (index * 100)).ms, duration: 400.ms)
                                .slideY(begin: 0.2, end: 0),
                          );
                        },
                        childCount: _languages.length,
                      ),
                    ),
                  ),
                ],
              ),
      ),
    );
  }
}
