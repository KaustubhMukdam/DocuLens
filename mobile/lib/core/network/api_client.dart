import 'package:dio/dio.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:pretty_dio_logger/pretty_dio_logger.dart';
import '../constants/api_constants.dart';
import '../storage/secure_storage.dart';
import 'api_interceptor.dart';

class ApiClient {
  static final ApiClient _instance = ApiClient._internal();
  factory ApiClient() => _instance;

  late final Dio _dio;

  ApiClient._internal() {
    _dio = Dio(
      BaseOptions(
        baseUrl: dotenv.env['BASE_URL'] ?? ApiConstants.baseUrl,
        connectTimeout: ApiConstants.connectTimeout,
        receiveTimeout: ApiConstants.receiveTimeout,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );

    // Add interceptors
    _dio.interceptors.add(ApiInterceptor());
    _dio.interceptors.add(
      PrettyDioLogger(
        requestHeader: true,
        requestBody: true,
        responseBody: true,
        responseHeader: false,
        error: true,
        compact: true,
      ),
    );
  }

  Dio get dio => _dio;

  // Auth API
  Future<Response> login(String username, String password) async {
    return await _dio.post(
      ApiConstants.login,
      data: FormData.fromMap({
        'username': username,
        'password': password,
      }),
      options: Options(
        contentType: 'application/x-www-form-urlencoded',
      ),
    );
  }

  Future<Response> register(String fullName, String email, String password) async {
    return await _dio.post(
      ApiConstants.register,
      data: {
        'full_name': fullName,
        'email': email,
        'password': password,
      },
    );
  }

  Future<Response> getUserProfile() async {
    return await _dio.get(ApiConstants.profile);
  }

  Future<Response> logout() async {
    return await _dio.post(ApiConstants.logout);
  }

  // Languages API
  Future<Response> getLanguages() async {
    return await _dio.get(ApiConstants.languages);
  }

  Future<Response> getLanguageDetail(String slug) async {
    return await _dio.get(ApiConstants.languageDetail(slug));
  }

  // Progress API
  Future<Response> getMyProgress() async {
    return await _dio.get(ApiConstants.myProgress);
  }

  Future<Response> getProgressStats() async {
    return await _dio.get(ApiConstants.progressStats);
  }
}
