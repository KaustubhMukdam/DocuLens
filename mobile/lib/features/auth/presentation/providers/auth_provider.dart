import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dio/dio.dart';
import '../../../../core/services/api_service.dart';
import '../../../../core/utils/logger.dart';
import 'auth_state.dart';

final apiServiceProvider = Provider((ref) => ApiService());

final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  final apiService = ref.watch(apiServiceProvider);
  return AuthNotifier(apiService);
});

class AuthNotifier extends StateNotifier<AuthState> {
  final ApiService _apiService;

  AuthNotifier(this._apiService) : super(const AuthInitial());

  // Get current user from state
  Map<String, dynamic>? get currentUser {
    final currentState = state;
    if (currentState is AuthAuthenticated) {
      return currentState.user;
    }
    return null;
  }

  // Check if user is authenticated
  bool get isAuthenticated => state is AuthAuthenticated;

  Future<void> login(String email, String password) async {
    try {
      state = const AuthLoading();
      logger.i('Attempting login for: $email');

      final response = await _apiService.login(email, password);

      if (response.statusCode == 200) {
        final data = response.data;
        final token = data['access_token'];
        final tokenType = data['token_type'];

        logger.i('Login successful, fetching user data...');

        // Get user data
        final userResponse = await _apiService.getCurrentUser(token);

        if (userResponse.statusCode == 200) {
          final userData = userResponse.data;

          state = AuthAuthenticated(
            token: token,
            tokenType: tokenType,
            user: userData,
          );

          logger.i('User authenticated: ${userData['email']}');
        } else {
          throw Exception('Failed to fetch user data');
        }
      } else {
        throw Exception('Login failed with status: ${response.statusCode}');
      }
    } on DioException catch (e) {
      logger.e('Login error: ${e.message}');

      String errorMessage = 'Login failed';

      if (e.response?.statusCode == 401) {
        errorMessage = 'Invalid email or password';
      } else if (e.response?.statusCode == 422) {
        errorMessage = 'Invalid input format. Please check your credentials.';
      } else if (e.response?.statusCode == 500) {
        errorMessage = 'Server error. Please try again later.';
      } else if (e.type == DioExceptionType.connectionTimeout) {
        errorMessage = 'Connection timeout. Check your network connection.';
      } else if (e.type == DioExceptionType.receiveTimeout) {
        errorMessage = 'Server took too long to respond.';
      } else if (e.response?.data != null) {
        final data = e.response!.data;
        if (data is Map && data.containsKey('detail')) {
          errorMessage = data['detail'].toString();
        } else if (data is Map && data.containsKey('error')) {
          errorMessage = data['error'].toString();
        }
      }

      state = AuthError(errorMessage);
    } catch (e) {
      logger.e('Unexpected error: $e');
      state = AuthError('An unexpected error occurred: ${e.toString()}');
    }
  }

  Future<void> signup({
    required String email,
    required String password,
    required String fullName,
    String? phoneNumber,
  }) async {
    try {
      state = const AuthLoading();
      logger.i('Attempting signup for: $email');

      final response = await _apiService.signup(
        email: email,
        password: password,
        fullName: fullName,
        phoneNumber: phoneNumber,
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        final data = response.data;
        final token = data['access_token'];
        final tokenType = data['token_type'];

        logger.i('Signup successful, fetching user data...');

        // Get user data
        final userResponse = await _apiService.getCurrentUser(token);

        if (userResponse.statusCode == 200) {
          final userData = userResponse.data;

          state = AuthAuthenticated(
            token: token,
            tokenType: tokenType,
            user: userData,
          );

          logger.i('User registered and authenticated: ${userData['email']}');
        } else {
          throw Exception('Failed to fetch user data');
        }
      } else {
        throw Exception('Signup failed with status: ${response.statusCode}');
      }
    } on DioException catch (e) {
      logger.e('Signup error: ${e.message}');

      String errorMessage = 'Signup failed';

      if (e.response?.statusCode == 400) {
        errorMessage = 'User already exists or invalid data';
      } else if (e.response?.statusCode == 422) {
        errorMessage = 'Invalid input format. Please check your information.';
      } else if (e.response?.statusCode == 500) {
        errorMessage = 'Server error. Please try again later.';
      } else if (e.type == DioExceptionType.connectionTimeout) {
        errorMessage = 'Connection timeout. Check your network connection.';
      } else if (e.response?.data != null) {
        final data = e.response!.data;
        if (data is Map && data.containsKey('detail')) {
          errorMessage = data['detail'].toString();
        } else if (data is Map && data.containsKey('error')) {
          errorMessage = data['error'].toString();
        }
      }

      state = AuthError(errorMessage);
    } catch (e) {
      logger.e('Unexpected error: $e');
      state = AuthError('An unexpected error occurred: ${e.toString()}');
    }
  }

  Future<void> logout() async {
    logger.i('User logged out');
    state = const AuthInitial();
  }
}
