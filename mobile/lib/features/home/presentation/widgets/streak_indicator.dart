import 'package:flutter/material.dart';
import '../../../../core/theme/app_theme.dart';

class StreakIndicator extends StatelessWidget {
  final int currentStreak;
  final int longestStreak;

  const StreakIndicator({
    super.key,
    required this.currentStreak,
    required this.longestStreak,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            (isDark ? AppTheme.darkWarning : AppTheme.lightWarning).withOpacity(0.2),
            (isDark ? AppTheme.darkWarning : AppTheme.lightWarning).withOpacity(0.1),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: (isDark ? AppTheme.darkWarning : AppTheme.lightWarning).withOpacity(0.3),
          width: 1,
        ),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: (isDark ? AppTheme.darkWarning : AppTheme.lightWarning).withOpacity(0.2),
              shape: BoxShape.circle,
            ),
            child: Icon(
              Icons.local_fire_department_rounded,
              color: isDark ? AppTheme.darkWarning : AppTheme.lightWarning,
              size: 32,
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '$currentStreak Day Streak!',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.w700,
                        color: isDark ? AppTheme.darkWarning : AppTheme.lightWarning,
                      ),
                ),
                const SizedBox(height: 4),
                Text(
                  'Longest: $longestStreak days',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: isDark ? AppTheme.darkTextSecondary : AppTheme.lightTextSecondary,
                      ),
                ),
              ],
            ),
          ),
          Text(
            '🔥',
            style: const TextStyle(fontSize: 40),
          ),
        ],
      ),
    );
  }
}
