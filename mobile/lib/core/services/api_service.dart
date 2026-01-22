import 'package:dio/dio.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import '../utils/logger.dart';

class ApiService {
  late final Dio _dio;
  static const int connectTimeout = 30000;
  static const int receiveTimeout = 30000;

  ApiService() {
    _dio = Dio(BaseOptions(
      baseUrl: dotenv.env['BASE_URL'] ?? 'http://10.37.155.246:8000/api/v1',
      connectTimeout: const Duration(milliseconds: connectTimeout),
      receiveTimeout: const Duration(milliseconds: receiveTimeout),
      headers: {
        'Accept': 'application/json',
      },
    ));

    _dio.interceptors.add(LogInterceptor(
      requestBody: true,
      responseBody: true,
      error: true,
      logPrint: (obj) => logger.i(obj),
    ));
  }

  Dio get dio => _dio;

  // Login
  Future<Response> login(String username, String password) async {
    try {
      return await _dio.post(
        '/auth/login',
        data: {
          'username': username,
          'password': password,
        },
        options: Options(
          contentType: Headers.formUrlEncodedContentType,
          headers: {
            'Accept': 'application/json',
          },
        ),
      );
    } catch (e) {
      logger.e('Login API error: $e');
      rethrow;
    }
  }

  // ✅ FIX: Signup with username field
  Future<Response> signup({
    required String email,
    required String password,
    required String fullName,
    String? phoneNumber,
  }) async {
    try {
      logger.i('Attempting signup for: $email');
      
      return await _dio.post(
        '/auth/register',  // ✅ Correct endpoint
        data: {
          'username': email,  // ✅ Use email as username
          'email': email,
          'password': password,
          'full_name': fullName,
          if (phoneNumber != null && phoneNumber.isNotEmpty) 
            'phone_number': phoneNumber,
        },
        options: Options(
          contentType: Headers.jsonContentType,  // ✅ Use JSON
          headers: {
            'Accept': 'application/json',
          },
        ),
      );
    } catch (e) {
      logger.e('Signup API error: $e');
      rethrow;
    }
  }

  // Get current user
  Future<Response> getCurrentUser(String token) async {
    try {
      return await _dio.get(
        '/users/me',
        options: Options(
          headers: {
            'Authorization': 'Bearer $token',
          },
        ),
      );
    } catch (e) {
      logger.e('Get current user error: $e');
      rethrow;
    }
  }

  // Upload document
  Future<Response> uploadDocument({
    required String token,
    required String filePath,
    String? fileName,
  }) async {
    try {
      FormData formData = FormData.fromMap({
        'file': await MultipartFile.fromFile(
          filePath,
          filename: fileName ?? filePath.split('/').last,
        ),
      });

      return await _dio.post(
        '/documents/upload',
        data: formData,
        options: Options(
          headers: {
            'Authorization': 'Bearer $token',
          },
        ),
      );
    } catch (e) {
      logger.e('Upload document error: $e');
      rethrow;
    }
  }

  // Get documents
  Future<Response> getDocuments(String token) async {
    try {
      return await _dio.get(
        '/documents',
        options: Options(
          headers: {
            'Authorization': 'Bearer $token',
          },
        ),
      );
    } catch (e) {
      logger.e('Get documents error: $e');
      rethrow;
    }
  }
}
