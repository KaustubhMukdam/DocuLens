# 📁 DocuLens - Folder Structure

Complete folder structure for the DocuLens project with detailed explanations.

---

## Overview

```
DocuLens/
├── backend/                 # FastAPI Backend
├── frontend/                # Flutter Frontend
├── docs/                    # Project Documentation
├── scripts/                 # Utility Scripts
├── .github/                 # GitHub Configuration
├── docker-compose.yml       # Multi-container Setup
├── .gitignore
├── LICENSE
└── README.md
```

---

## Backend Structure

```
backend/
│
├── app/                                    # Main application directory
│   ├── __init__.py
│   ├── main.py                            # FastAPI app entry point
│   │
│   ├── api/                               # API routes
│   │   ├── __init__.py
│   │   ├── deps.py                        # Common dependencies (get_db, get_current_user)
│   │   └── v1/                            # API version 1
│   │       ├── __init__.py
│   │       ├── router.py                  # Main router combining all routes
│   │       ├── auth.py                    # Authentication endpoints
│   │       │   # POST /register, /login, /logout, /refresh
│   │       ├── users.py                   # User management endpoints
│   │       │   # GET /me, PUT /me, DELETE /me
│   │       ├── languages.py               # Programming languages endpoints
│   │       │   # GET /languages, GET /languages/{slug}
│   │       ├── docs.py                    # Documentation endpoints
│   │       │   # GET /docs/{lang}/sections, GET /docs/sections/{id}
│   │       ├── learning_paths.py          # Learning path endpoints
│   │       │   # POST /learning-paths, GET /learning-paths/my-paths
│   │       ├── progress.py                # Progress tracking endpoints
│   │       │   # POST /progress/mark-complete, GET /progress/stats
│   │       ├── problems.py                # Practice problems endpoints
│   │       │   # GET /problems/by-section/{id}, GET /problems/recommended
│   │       ├── search.py                  # Search endpoints
│   │       │   # GET /search?q=...
│   │       ├── bookmarks.py               # Bookmarks endpoints
│   │       │   # POST /bookmarks, GET /bookmarks, DELETE /bookmarks/{id}
│   │       ├── notes.py                   # User notes endpoints
│   │       │   # POST /notes, PUT /notes/{id}, DELETE /notes/{id}
│   │       ├── community.py               # Community features endpoints
│   │       │   # GET /discussions, POST /discussions, POST /discussions/{id}/comments
│   │       └── admin.py                   # Admin endpoints (future)
│   │
│   ├── core/                              # Core configurations
│   │   ├── __init__.py
│   │   ├── config.py                      # Settings class (Pydantic BaseSettings)
│   │   │   # Database URL, API keys, Secret keys, Environment
│   │   ├── security.py                    # JWT, password hashing utilities
│   │   │   # create_access_token(), verify_password(), get_password_hash()
│   │   ├── logging.py                     # Logging configuration (Loguru)
│   │   └── exceptions.py                  # Custom exception classes
│   │       # NotFoundException, UnauthorizedException, etc.
│   │
│   ├── models/                            # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── base.py                        # Base model with common fields
│   │   │   # id, created_at, updated_at
│   │   ├── user.py                        # User model
│   │   │   # id, email, username, password_hash, full_name, avatar_url,
│   │   │   # skill_level, preferred_language, is_active, is_premium
│   │   ├── language.py                    # Language model
│   │   │   # id, name, slug, official_doc_url, logo_url, description,
│   │   │   # version, last_updated
│   │   ├── doc_section.py                 # Documentation section model
│   │   │   # id, language_id, parent_id, title, slug, content_raw,
│   │   │   # content_summary, source_url, order_index, estimated_time_minutes,
│   │   │   # difficulty, is_quick_path, is_deep_path
│   │   ├── code_example.py                # Code example model
│   │   │   # id, doc_section_id, title, code, language, explanation,
│   │   │   # output, is_runnable, order_index
│   │   ├── learning_path.py               # Learning path model
│   │   │   # id, user_id, language_id, path_type, status,
│   │   │   # progress_percentage, started_at, completed_at
│   │   ├── user_progress.py               # User progress model
│   │   │   # id, user_id, doc_section_id, is_completed,
│   │   │   # time_spent_seconds, completed_at, notes
│   │   ├── practice_problem.py            # Practice problem model
│   │   │   # id, doc_section_id, title, platform, problem_url,
│   │   │   # difficulty, topics
│   │   ├── video_resource.py              # Video resource model
│   │   │   # id, doc_section_id, title, platform, video_url,
│   │   │   # thumbnail_url, duration_seconds, channel_name, views
│   │   ├── bookmark.py                    # Bookmark model
│   │   │   # id, user_id, doc_section_id, notes
│   │   ├── user_note.py                   # User note model
│   │   │   # id, user_id, doc_section_id, content, is_public
│   │   ├── discussion.py                  # Discussion model
│   │   │   # id, doc_section_id, user_id, title, content,
│   │   │   # upvotes, is_solved
│   │   └── discussion_comment.py          # Discussion comment model
│   │       # id, discussion_id, user_id, content, upvotes, is_solution
│   │
│   ├── schemas/                           # Pydantic schemas (Request/Response DTOs)
│   │   ├── __init__.py
│   │   ├── auth.py                        # Auth schemas
│   │   │   # LoginRequest, RegisterRequest, TokenResponse, RefreshRequest
│   │   ├── user.py                        # User schemas
│   │   │   # UserCreate, UserUpdate, UserResponse, UserInDB
│   │   ├── language.py                    # Language schemas
│   │   │   # LanguageResponse, LanguageDetail, LanguageCreate
│   │   ├── doc_section.py                 # Doc section schemas
│   │   │   # DocSectionResponse, DocSectionDetail, SectionSummary
│   │   ├── learning_path.py               # Learning path schemas
│   │   │   # LearningPathCreate, LearningPathResponse, PathProgress
│   │   ├── progress.py                    # Progress schemas
│   │   │   # ProgressUpdate, ProgressStats, MarkCompleteRequest
│   │   ├── problem.py                     # Problem schemas
│   │   │   # ProblemResponse, ProblemDetail
│   │   ├── bookmark.py                    # Bookmark schemas
│   │   │   # BookmarkCreate, BookmarkResponse
│   │   ├── note.py                        # Note schemas
│   │   │   # NoteCreate, NoteUpdate, NoteResponse
│   │   ├── discussion.py                  # Discussion schemas
│   │   │   # DiscussionCreate, DiscussionResponse, CommentCreate
│   │   └── response.py                    # Common response schemas
│   │       # SuccessResponse, ErrorResponse, PaginatedResponse
│   │
│   ├── services/                          # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py                # Authentication logic
│   │   │   # register_user(), login_user(), refresh_token()
│   │   ├── user_service.py                # User management logic
│   │   │   # get_user(), update_user(), delete_user()
│   │   ├── doc_service.py                 # Documentation logic
│   │   │   # get_sections(), get_section_by_id(), search_sections()
│   │   ├── learning_path_service.py       # Learning path logic
│   │   │   # create_path(), get_user_paths(), calculate_progress()
│   │   ├── progress_service.py            # Progress tracking logic
│   │   │   # mark_complete(), get_stats(), calculate_streak()
│   │   ├── ai_service.py                  # AI/LLM integration
│   │   │   # summarize(), groq_summarize(), claude_summarize()
│   │   ├── scraper_service.py             # Web scraping orchestration
│   │   │   # trigger_scrape(), process_scraped_content()
│   │   ├── search_service.py              # Search logic
│   │   │   # semantic_search(), filter_search(), suggest_search()
│   │   ├── recommendation_service.py      # Recommendation logic
│   │   │   # recommend_next_section(), recommend_problems()
│   │   └── email_service.py               # Email sending logic
│   │       # send_welcome_email(), send_password_reset()
│   │
│   ├── db/                                # Database configuration
│   │   ├── __init__.py
│   │   ├── base.py                        # Import all models for Alembic
│   │   ├── session.py                     # Database session management
│   │   │   # get_db() dependency, async session factory
│   │   └── init_db.py                     # Database initialization
│   │       # create_first_superuser(), seed_initial_data()
│   │
│   ├── crud/                              # CRUD operations (Database access)
│   │   ├── __init__.py
│   │   ├── base.py                        # Base CRUD class with generic methods
│   │   │   # get(), get_multi(), create(), update(), delete()
│   │   ├── user.py                        # User CRUD
│   │   │   # get_by_email(), get_by_username(), authenticate()
│   │   ├── language.py                    # Language CRUD
│   │   │   # get_by_slug(), get_all_active()
│   │   ├── doc_section.py                 # Doc section CRUD
│   │   │   # get_by_language(), get_by_path_type(), search()
│   │   ├── learning_path.py               # Learning path CRUD
│   │   │   # get_user_paths(), get_active_path()
│   │   ├── progress.py                    # Progress CRUD
│   │   │   # get_user_progress(), update_progress()
│   │   ├── bookmark.py                    # Bookmark CRUD
│   │   │   # get_user_bookmarks(), create_bookmark()
│   │   └── discussion.py                  # Discussion CRUD
│   │       # get_by_section(), create_discussion(), add_comment()
│   │
│   ├── scrapers/                          # Web scraping modules
│   │   ├── __init__.py
│   │   ├── base_scraper.py                # Abstract base scraper class
│   │   │   # scrape(), parse(), validate(), save()
│   │   ├── python_scraper.py              # Python documentation scraper
│   │   │   # Scrapes docs.python.org
│   │   ├── flutter_scraper.py             # Flutter documentation scraper
│   │   │   # Scrapes docs.flutter.dev
│   │   ├── javascript_scraper.py          # JavaScript (MDN) scraper
│   │   │   # Scrapes developer.mozilla.org
│   │   ├── react_scraper.py               # React documentation scraper
│   │   │   # Scrapes react.dev
│   │   ├── fastapi_scraper.py             # FastAPI documentation scraper
│   │   │   # Scrapes fastapi.tiangolo.com
│   │   └── utils.py                       # Scraping utilities
│   │       # clean_html(), extract_code_blocks(), rate_limiter()
│   │
│   ├── tasks/                             # Celery background tasks
│   │   ├── __init__.py
│   │   ├── celery_app.py                  # Celery application configuration
│   │   ├── scraping_tasks.py              # Scraping tasks
│   │   │   # scrape_documentation(), update_documentation()
│   │   ├── ai_tasks.py                    # AI processing tasks
│   │   │   # summarize_section(), generate_learning_path()
│   │   ├── email_tasks.py                 # Email tasks
│   │   │   # send_welcome_email(), send_notification()
│   │   ├── cleanup_tasks.py               # Maintenance tasks
│   │   │   # cleanup_old_sessions(), archive_old_data()
│   │   └── analytics_tasks.py             # Analytics tasks
│   │       # calculate_daily_stats(), generate_reports()
│   │
│   ├── utils/                             # Utility functions
│   │   ├── __init__.py
│   │   ├── text_processing.py             # Text utilities
│   │   │   # clean_text(), truncate(), word_count()
│   │   ├── time_estimation.py             # Time estimation utilities
│   │   │   # estimate_reading_time(), calculate_completion_time()
│   │   ├── validators.py                  # Custom validators
│   │   │   # validate_email(), validate_password_strength()
│   │   ├── cache.py                       # Caching utilities
│   │   │   # cache_decorator(), invalidate_cache()
│   │   └── helpers.py                     # General helpers
│   │       # generate_slug(), format_date(), paginate()
│   │
│   ├── middleware/                        # Custom middleware
│   │   ├── __init__.py
│   │   ├── rate_limit.py                  # Rate limiting middleware
│   │   ├── cors.py                        # CORS middleware configuration
│   │   ├── error_handler.py               # Global error handling
│   │   └── request_logger.py              # Request logging middleware
│   │
│   └── integrations/                      # Third-party integrations
│       ├── __init__.py
│       ├── groq_client.py                 # Groq API client
│       ├── claude_client.py               # Claude API client (backup)
│       ├── youtube_client.py              # YouTube Data API client
│       ├── leetcode_client.py             # LeetCode API client
│       ├── github_client.py               # GitHub API client
│       └── sendgrid_client.py             # SendGrid email client
│
├── tests/                                 # Test directory
│   ├── __init__.py
│   ├── conftest.py                        # Pytest fixtures and configuration
│   │   # db_session, test_client, test_user fixtures
│   ├── unit/                              # Unit tests
│   │   ├── __init__.py
│   │   ├── test_auth_service.py
│   │   ├── test_ai_service.py
│   │   ├── test_doc_service.py
│   │   └── test_utils.py
│   ├── integration/                       # Integration tests
│   │   ├── __init__.py
│   │   ├── test_auth_endpoints.py
│   │   ├── test_doc_endpoints.py
│   │   ├── test_learning_paths.py
│   │   └── test_database.py
│   └── fixtures/                          # Test data
│       ├── __init__.py
│       ├── sample_docs.py
│       └── sample_users.py
│
├── alembic/                               # Database migrations
│   ├── versions/                          # Migration files
│   │   ├── 001_initial_migration.py
│   │   ├── 002_add_bookmarks.py
│   │   └── 003_add_discussions.py
│   ├── env.py                             # Alembic environment configuration
│   ├── script.py.mako                     # Migration template
│   └── alembic.ini                        # Alembic configuration
│
├── scripts/                               # Utility scripts
│   ├── __init__.py
│   ├── init_db.py                         # Initialize database
│   ├── seed_data.py                       # Seed initial data
│   │   # python scripts/seed_data.py
│   ├── run_scraper.py                     # Run scrapers manually
│   │   # python scripts/run_scraper.py --language python
│   ├── backup_db.py                       # Backup database
│   ├── migrate_data.py                    # Data migration script
│   └── generate_summaries.py              # Batch generate AI summaries
│
├── logs/                                  # Log files (gitignored)
│   ├── app.log
│   ├── celery.log
│   └── scraper.log
│
├── requirements.txt                       # Production dependencies
├── requirements-dev.txt                   # Development dependencies
│   # pytest, black, ruff, mypy, faker, factory-boy
│
├── Dockerfile                             # Docker configuration for backend
├── docker-compose.yml                     # Local development setup
├── .dockerignore
│
├── .env.example                           # Environment variables template
│   # DATABASE_URL, REDIS_URL, GROQ_API_KEY, SECRET_KEY, etc.
├── .env                                   # Actual environment variables (gitignored)
│
├── .gitignore                             # Git ignore rules
├── pyproject.toml                         # Python project configuration
│   # Black, Ruff, MyPy configuration
├── pytest.ini                             # Pytest configuration
├── mypy.ini                               # MyPy configuration
│
└── README.md                              # Backend-specific README
```

---

## Frontend Structure

```
frontend/
│
├── lib/                                   # Main application code
│   ├── main.dart                          # App entry point
│   │   # void main() { runApp(MyApp()); }
│   │
│   ├── app/                               # App configuration
│   │   ├── app.dart                       # Main app widget (MaterialApp/ProviderScope)
│   │   └── routes.dart                    # App routing configuration (GoRouter)
│   │       # Route definitions, redirects, error handling
│   │
│   ├── core/                              # Core utilities and configurations
│   │   ├── constants/                     # Constant values
│   │   │   ├── api_constants.dart         # API endpoints, base URLs
│   │   │   ├── app_constants.dart         # App-wide constants
│   │   │   ├── storage_keys.dart          # Local storage keys
│   │   │   └── theme_constants.dart       # Theme-related constants
│   │   │
│   │   ├── theme/                         # App theming
│   │   │   ├── app_theme.dart             # Theme provider/controller
│   │   │   ├── light_theme.dart           # Light theme configuration
│   │   │   ├── dark_theme.dart            # Dark theme configuration
│   │   │   ├── app_colors.dart            # Color palette
│   │   │   └── app_text_styles.dart       # Typography styles
│   │   │
│   │   ├── utils/                         # Utility functions
│   │   │   ├── date_utils.dart            # Date formatting utilities
│   │   │   ├── validators.dart            # Form validators
│   │   │   ├── extensions.dart            # Dart extensions
│   │   │   │   # String extensions, BuildContext extensions
│   │   │   ├── helpers.dart               # General helper functions
│   │   │   └── formatters.dart            # Text input formatters
│   │   │
│   │   └── network/                       # Networking configuration
│   │       ├── dio_client.dart            # Dio client setup
│   │       ├── interceptors.dart          # HTTP interceptors
│   │       │   # Auth interceptor, logging interceptor, error interceptor
│   │       ├── api_endpoints.dart         # API endpoint definitions
│   │       └── api_exceptions.dart        # Custom API exceptions
│   │
│   ├── data/                              # Data layer
│   │   ├── models/                        # Data models
│   │   │   ├── user_model.dart            # User model
│   │   │   │   # fromJson(), toJson(), copyWith()
│   │   │   ├── language_model.dart        # Programming language model
│   │   │   ├── doc_section_model.dart     # Documentation section model
│   │   │   ├── learning_path_model.dart   # Learning path model
│   │   │   ├── progress_model.dart        # Progress model
│   │   │   ├── problem_model.dart         # Practice problem model
│   │   │   ├── video_model.dart           # Video resource model
│   │   │   ├── bookmark_model.dart        # Bookmark model
│   │   │   └── discussion_model.dart      # Discussion model
│   │   │
│   │   ├── repositories/                  # Data repositories
│   │   │   ├── auth_repository.dart       # Authentication repository
│   │   │   │   # login(), register(), logout(), refreshToken()
│   │   │   ├── user_repository.dart       # User repository
│   │   │   │   # getCurrentUser(), updateUser(), deleteUser()
│   │   │   ├── doc_repository.dart        # Documentation repository
│   │   │   │   # getLanguages(), getSections(), getSectionDetail()
│   │   │   ├── learning_path_repository.dart  # Learning path repository
│   │   │   │   # createPath(), getUserPaths(), getPathDetail()
│   │   │   ├── progress_repository.dart   # Progress repository
│   │   │   │   # markComplete(), getStats(), getProgress()
│   │   │   └── search_repository.dart     # Search repository
│   │   │       # search(), getFilters(), getRecommendations()
│   │   │
│   │   ├── providers/                     # API providers (Retrofit clients)
│   │   │   ├── auth_provider.dart         # Auth API provider
│   │   │   │   # @POST('/auth/login'), @POST('/auth/register')
│   │   │   ├── user_provider.dart         # User API provider
│   │   │   ├── doc_provider.dart          # Documentation API provider
│   │   │   ├── learning_path_provider.dart # Learning path API provider
│   │   │   └── progress_provider.dart     # Progress API provider
│   │   │
│   │   └── local/                         # Local data sources
│   │       ├── storage_service.dart       # Local storage service (Hive)
│   │       ├── cache_service.dart         # Cache service
│   │       └── secure_storage_service.dart # Secure storage (tokens)
│   │
│   ├── features/                          # Feature modules (Clean Architecture)
│   │   │
│   │   ├── auth/                          # Authentication feature
│   │   │   ├── presentation/
│   │   │   │   ├── pages/
│   │   │   │   │   ├── login_page.dart
│   │   │   │   │   ├── register_page.dart
│   │   │   │   │   ├── forgot_password_page.dart
│   │   │   │   │   └── onboarding_page.dart
│   │   │   │   ├── widgets/
│   │   │   │   │   ├── bookmark_card.dart
│   │   │   │   │   └── bookmark_list.dart
│   │   │   │   └── providers/
│   │   │   │       └── bookmarks_provider.dart
│   │   │   └── domain/
│   │   │       └── usecases/
│   │   │           ├── add_bookmark_usecase.dart
│   │   │           └── remove_bookmark_usecase.dart
│   │   │
│   │   ├── notes/                         # Notes feature
│   │   │   ├── presentation/
│   │   │   │   ├── pages/
│   │   │   │   │   ├── notes_page.dart
│   │   │   │   │   └── note_editor_page.dart
│   │   │   │   ├── widgets/
│   │   │   │   │   ├── note_card.dart
│   │   │   │   │   ├── note_editor.dart
│   │   │   │   │   └── note_filter.dart
│   │   │   │   └── providers/
│   │   │   │       └── notes_provider.dart
│   │   │   └── domain/
│   │   │       └── usecases/
│   │   │           ├── create_note_usecase.dart
│   │   │           └── update_note_usecase.dart
│   │   │
│   │   ├── community/                     # Community feature
│   │   │   ├── presentation/
│   │   │   │   ├── pages/
│   │   │   │   │   ├── discussions_page.dart
│   │   │   │   │   └── discussion_detail_page.dart
│   │   │   │   ├── widgets/
│   │   │   │   │   ├── discussion_card.dart
│   │   │   │   │   ├── comment_widget.dart
│   │   │   │   │   └── create_discussion_form.dart
│   │   │   │   └── providers/
│   │   │   │       └── community_provider.dart
│   │   │   └── domain/
│   │   │       └── usecases/
│   │   │           └── create_discussion_usecase.dart
│   │   │
│   │   └── settings/                      # Settings feature
│   │       ├── presentation/
│   │       │   ├── pages/
│   │       │   │   ├── settings_page.dart
│   │       │   │   ├── profile_page.dart
│   │       │   │   ├── preferences_page.dart
│   │       │   │   └── about_page.dart
│   │       │   ├── widgets/
│   │       │   │   ├── settings_tile.dart
│   │       │   │   ├── theme_switcher.dart
│   │       │   │   └── language_selector.dart
│   │       │   └── providers/
│   │       │       └── settings_provider.dart
│   │       └── domain/
│   │           └── usecases/
│   │               └── update_preferences_usecase.dart
│   │
│   └── shared/                            # Shared widgets and utilities
│       ├── widgets/                       # Reusable widgets
│       │   ├── custom_button.dart         # Custom button widget
│       │   ├── custom_textfield.dart      # Custom text field
│       │   ├── loading_indicator.dart     # Loading spinner
│       │   ├── error_widget.dart          # Error display widget
│       │   ├── empty_state_widget.dart    # Empty state display
│       │   ├── bottom_nav_bar.dart        # Bottom navigation bar
│       │   ├── app_bar_widget.dart        # Custom app bar
│       │   ├── avatar_widget.dart         # User avatar
│       │   ├── badge_widget.dart          # Badge/chip widget
│       │   ├── card_widget.dart           # Custom card
│       │   ├── dialog_widget.dart         # Custom dialogs
│       │   └── snackbar_widget.dart       # Custom snackbar
│       │
│       ├── animations/                    # Reusable animations
│       │   ├── fade_in_animation.dart
│       │   ├── slide_animation.dart
│       │   └── scale_animation.dart
│       │
│       └── mixins/                        # Reusable mixins
│           ├── validation_mixin.dart
│           └── loading_mixin.dart
│
├── assets/                                # Static assets
│   ├── images/                            # Image files
│   │   ├── logo.png
│   │   ├── logo_dark.png
│   │   ├── onboarding/
│   │   │   ├── onboarding_1.png
│   │   │   ├── onboarding_2.png
│   │   │   └── onboarding_3.png
│   │   ├── placeholders/
│   │   │   ├── avatar_placeholder.png
│   │   │   └── image_placeholder.png
│   │   └── languages/                     # Language logos
│   │       ├── python.png
│   │       ├── flutter.png
│   │       ├── javascript.png
│   │       └── react.png
│   │
│   ├── icons/                             # Custom icons
│   │   ├── app_icon.png
│   │   └── custom_icons.ttf
│   │
│   ├── animations/                        # Lottie animations
│   │   ├── loading.json
│   │   ├── success.json
│   │   ├── error.json
│   │   └── empty_state.json
│   │
│   └── fonts/                             # Custom fonts (if needed)
│       └── custom_font.ttf
│
├── test/                                  # Test directory
│   ├── unit/                              # Unit tests
│   │   ├── models/
│   │   │   └── user_model_test.dart
│   │   ├── repositories/
│   │   │   └── auth_repository_test.dart
│   │   └── utils/
│   │       └── validators_test.dart
│   │
│   ├── widget/                            # Widget tests
│   │   ├── auth/
│   │   │   └── login_page_test.dart
│   │   └── shared/
│   │       └── custom_button_test.dart
│   │
│   ├── integration/                       # Integration tests
│   │   └── app_test.dart
│   │
│   └── fixtures/                          # Test fixtures
│       ├── user_fixture.dart
│       └── mock_data.dart
│
├── android/                               # Android-specific files
│   ├── app/
│   │   ├── src/
│   │   │   └── main/
│   │   │       ├── AndroidManifest.xml
│   │   │       └── res/
│   │   └── build.gradle
│   └── build.gradle
│
├── ios/                                   # iOS-specific files
│   ├── Runner/
│   │   ├── Info.plist
│   │   └── Assets.xcassets/
│   └── Podfile
│
├── web/                                   # Web-specific files
│   ├── index.html
│   ├── manifest.json
│   └── icons/
│
├── linux/                                 # Linux-specific (future)
├── macos/                                 # macOS-specific (future)
├── windows/                               # Windows-specific (future)
│
├── pubspec.yaml                           # Flutter dependencies
├── pubspec.lock                           # Locked dependencies
│
├── analysis_options.yaml                  # Dart analyzer configuration
│
├── .env.example                           # Environment variables template
├── .env                                   # Actual environment (gitignored)
│
├── .gitignore                             # Git ignore rules
├── .metadata                              # Flutter metadata
│
└── README.md                              # Frontend-specific README
```

---

## Documentation Structure

```
docs/
│
├── README.md                              # Documentation overview
│
├── SDLC.md                                # Software Development Life Cycle
│   # Complete SDLC with all 10 phases
│
├── PRD.md                                 # Product Requirements Document
│   # Product overview, features, success metrics
│
├── TECH_STACK.md                          # Technology Stack
│   # Backend, frontend, DevOps stack details
│
├── FOLDER_STRUCTURE.md                    # This file
│   # Complete project folder structure
│
├── API.md                                 # API Documentation
│   # All endpoints, request/response schemas
│
├── DATABASE_SCHEMA.md                     # Database Schema
│   # ERD, table definitions, relationships
│
├── ARCHITECTURE.md                        # System Architecture
│   # High-level architecture, design patterns
│
├── DEPLOYMENT.md                          # Deployment Guide
│   # How to deploy to various environments
│
├── CONTRIBUTING.md                        # Contribution Guidelines
│   # How to contribute, code standards
│
├── TESTING.md                             # Testing Strategy
│   # Unit, integration, e2e testing guides
│
├── SECURITY.md                            # Security Guidelines
│   # Security best practices, vulnerability reporting
│
├── CHANGELOG.md                           # Change Log
│   # Version history, what changed in each release
│
└── guides/                                # Additional guides
    ├── SETUP.md                           # Setup guide for developers
    ├── CODING_STANDARDS.md                # Code style guide
    ├── GIT_WORKFLOW.md                    # Git branching strategy
    └── TROUBLESHOOTING.md                 # Common issues and solutions
```

---

## Scripts Structure

```
scripts/
│
├── setup/                                 # Setup scripts
│   ├── setup_dev.sh                       # Setup development environment
│   ├── install_dependencies.sh            # Install all dependencies
│   └── setup_git_hooks.sh                 # Setup pre-commit hooks
│
├── database/                              # Database scripts
│   ├── create_db.sh                       # Create database
│   ├── backup_db.sh                       # Backup database
│   ├── restore_db.sh                      # Restore from backup
│   └── reset_db.sh                        # Reset database (dev only)
│
├── deployment/                            # Deployment scripts
│   ├── deploy_staging.sh                  # Deploy to staging
│   ├── deploy_production.sh               # Deploy to production
│   └── rollback.sh                        # Rollback deployment
│
├── maintenance/                           # Maintenance scripts
│   ├── cleanup_logs.sh                    # Clean up old logs
│   ├── archive_old_data.sh                # Archive old data
│   └── health_check.sh                    # System health check
│
└── data/                                  # Data scripts
    ├── import_data.py                     # Import data
    ├── export_data.py                     # Export data
    └── migrate_data.py                    # Migrate data between versions
```

---

## GitHub Configuration

```
.github/
│
├── workflows/                             # GitHub Actions workflows
│   ├── backend-ci.yml                     # Backend CI pipeline
│   │   # Runs on: push, pull_request to main/develop
│   │   # Jobs: lint, test, build
│   │
│   ├── frontend-ci.yml                    # Frontend CI pipeline
│   │   # Runs on: push, pull_request to main/develop
│   │   # Jobs: analyze, test, build
│   │
│   ├── deploy-staging.yml                 # Deploy to staging
│   │   # Runs on: push to develop
│   │   # Jobs: build, deploy
│   │
│   ├── deploy-production.yml              # Deploy to production
│   │   # Runs on: push to main (with tag)
│   │   # Jobs: build, deploy, notify
│   │
│   ├── security-scan.yml                  # Security scanning
│   │   # Runs on: schedule (weekly)
│   │   # Jobs: dependency check, code scan
│   │
│   └── release.yml                        # Create release
│       # Runs on: tag push
│       # Jobs: build, create release, upload assets
│
├── ISSUE_TEMPLATE/                        # Issue templates
│   ├── bug_report.md                      # Bug report template
│   ├── feature_request.md                 # Feature request template
│   └── question.md                        # Question template
│
├── PULL_REQUEST_TEMPLATE.md               # PR template
│
├── dependabot.yml                         # Dependabot configuration
│   # Auto update dependencies
│
└── CODE_OF_CONDUCT.md                     # Code of conduct
```

---

## Docker Configuration

### Root docker-compose.yml

```yaml
# docker-compose.yml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: doculens_db
    environment:
      POSTGRES_USER: doculens
      POSTGRES_PASSWORD: doculens_password
      POSTGRES_DB: doculens
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - doculens_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U doculens"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: doculens_redis
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    networks:
      - doculens_network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  # RabbitMQ Message Broker
  rabbitmq:
    image: rabbitmq:3.12-management-alpine
    container_name: doculens_rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: doculens
      RABBITMQ_DEFAULT_PASS: doculens_password
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    ports:
      - "5672:5672"    # AMQP port
      - "15672:15672"  # Management UI
    networks:
      - doculens_network
    healthcheck:
      test: rabbitmq-diagnostics -q ping
      interval: 30s
      timeout: 10s
      retries: 5

  # FastAPI Backend
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: doculens_backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://doculens:doculens_password@db:5432/doculens
      - REDIS_URL=redis://redis:6379
      - RABBITMQ_URL=amqp://doculens:doculens_password@rabbitmq:5672/
      - GROQ_API_KEY=${GROQ_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    networks:
      - doculens_network

  # Celery Worker
  celery_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: doculens_celery_worker
    command: celery -A app.tasks.celery_app worker --loglevel=info
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://doculens:doculens_password@db:5432/doculens
      - REDIS_URL=redis://redis:6379
      - RABBITMQ_URL=amqp://doculens:doculens_password@rabbitmq:5672/
      - GROQ_API_KEY=${GROQ_API_KEY}
    depends_on:
      - backend
      - rabbitmq
      - redis
    networks:
      - doculens_network

  # Celery Beat (Scheduler)
  celery_beat:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: doculens_celery_beat
    command: celery -A app.tasks.celery_app beat --loglevel=info
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://doculens:doculens_password@db:5432/doculens
      - REDIS_URL=redis://redis:6379
      - RABBITMQ_URL=amqp://doculens:doculens_password@rabbitmq:5672/
    depends_on:
      - backend
      - rabbitmq
    networks:
      - doculens_network

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: doculens_nginx
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend
    networks:
      - doculens_network

networks:
  doculens_network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
  rabbitmq_data:
```

---

## Environment Files

### Backend .env.example

```bash
# .env.example

# Environment
ENVIRONMENT=development  # development, staging, production

# Application
APP_NAME=DocuLens
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production

# Database
DATABASE_URL=postgresql://doculens:password@localhost:5432/doculens
DATABASE_ECHO=False  # Set to True to log SQL queries

# Redis
REDIS_URL=redis://localhost:6379/0

# RabbitMQ / Celery
RABBITMQ_URL=amqp://doculens:password@localhost:5672/
CELERY_BROKER_URL=amqp://doculens:password@localhost:5672/
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# JWT
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30

# AI APIs
GROQ_API_KEY=your-groq-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here  # Backup/Premium

# External APIs
YOUTUBE_API_KEY=your-youtube-api-key-here
GITHUB_TOKEN=your-github-token-here

# OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Email
SENDGRID_API_KEY=your-sendgrid-api-key
FROM_EMAIL=noreply@doculens.dev
FROM_NAME=DocuLens

# Storage
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_S3_BUCKET=doculens-content
AWS_REGION=us-east-1

# Or Cloudflare R2
R2_ACCESS_KEY_ID=your-r2-access-key
R2_SECRET_ACCESS_KEY=your-r2-secret-key
R2_BUCKET=doculens-content
R2_ENDPOINT=https://your-account-id.r2.cloudflarestorage.com

# Monitoring
SENTRY_DSN=your-sentry-dsn

# CORS
CORS_ORIGINS=["http://localhost:3000", "https://doculens.dev"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
```

### Frontend .env.example

```bash
# .env.example

# API
API_BASE_URL=http://localhost:8000/api/v1
API_TIMEOUT=30000  # milliseconds

# OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GITHUB_CLIENT_ID=your-github-client-id

# Analytics
GA_MEASUREMENT_ID=G-XXXXXXXXXX
MIXPANEL_TOKEN=your-mixpanel-token

# Sentry
SENTRY_DSN=your-sentry-dsn

# Feature Flags
ENABLE_PREMIUM_FEATURES=false
ENABLE_OFFLINE_MODE=false
ENABLE_CODE_PLAYGROUND=false

# App Configuration
APP_NAME=DocuLens
APP_VERSION=1.0.0
```

---

## Key Files Explanation

### Backend

#### `app/main.py`
```python
"""
FastAPI application entry point.
Sets up the app, middleware, routes, and startup/shutdown events.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    # Initialize database connection pool, etc.
    pass

@app.on_event("shutdown")
async def shutdown():
    # Close database connections, etc.
    pass
```

#### `app/core/config.py`
```python
"""
Application configuration using Pydantic settings.
Reads from environment variables.
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "DocuLens"
    DEBUG: bool = False
    SECRET_KEY: str
    DATABASE_URL: str
    REDIS_URL: str
    GROQ_API_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### Frontend

#### `lib/main.dart`
```dart
/// Main entry point for the DocuLens Flutter app.

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'app/app.dart';

void main() {
  runApp(
    const ProviderScope(
      child: DocuLensApp(),
    ),
  );
}
```

#### `lib/app/app.dart`
```dart
/// Main app widget with theme and routing configuration.

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'routes.dart';
import '../core/theme/app_theme.dart';

class DocuLensApp extends ConsumerWidget {
  const DocuLensApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);
    final themeMode = ref.watch(themeModeProvider);

    return MaterialApp.router(
      title: 'DocuLens',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: themeMode,
      routerConfig: router,
    );
  }
}
```

---

## Naming Conventions

### Backend (Python)

```python
# Files: snake_case
user_service.py
auth_repository.py

# Classes: PascalCase
class UserService:
class AuthRepository:

# Functions/Methods: snake_case
def get_user_by_id():
def create_access_token():

# Constants: UPPER_SNAKE_CASE
MAX_LOGIN_ATTEMPTS = 5
DEFAULT_TIMEOUT = 30

# Private: _prefix
def _internal_helper():
_private_variable = "value"
```

### Frontend (Dart)

```dart
// Files: snake_case
user_repository.dart
auth_provider.dart

// Classes: PascalCase
class UserRepository {}
class AuthProvider {}

// Functions/Methods: camelCase
void getUserById() {}
Future<void> createToken() async {}

// Constants: lowerCamelCase or UPPER_SNAKE_CASE
const int maxLoginAttempts = 5;
const int DEFAULT_TIMEOUT = 30;

// Private: _prefix
void _internalHelper() {}
final String _privateVariable = "value";

// Widgets: PascalCase + Widget suffix
class LoginPageWidget extends StatelessWidget {}
class CustomButtonWidget extends StatelessWidget {}
```

---

## Best Practices

### 1. Keep Folders Organized
- Group related files together
- Don't create too deep nesting (max 4-5 levels)
- Use index files to re-export common modules

### 2. Separation of Concerns
- **Backend**: Models → CRUD → Services → API
- **Frontend**: Data → Domain → Presentation (Clean Architecture)

### 3. Testing Structure Mirrors Source
- `tests/unit/services/` mirrors `app/services/`
- `test/widget/auth/` mirrors `lib/features/auth/presentation/pages/`

### 4. Documentation
- README.md in each major directory
- Inline comments for complex logic
- Docstrings for all public functions/classes

### 5. Environment-Specific Configs
- Never commit `.env` files
- Always provide `.env.example`
- Use different configs for dev/staging/prod

---

**Last Updated**: January 2026  
**Maintained By**: Kaustubh Mukdam

For questions or suggestions about the folder structure, please open an issue on GitHub.   ├── login_form.dart
│   │   │   │   │   ├── register_form.dart
│   │   │   │   │   ├── social_login_buttons.dart
│   │   │   │   │   └── password_field.dart
│   │   │   │   └── providers/
│   │   │   │       ├── auth_state_provider.dart
│   │   │   │       ├── login_form_provider.dart
│   │   │   │       └── register_form_provider.dart
│   │   │   └── domain/
│   │   │       └── usecases/
│   │   │           ├── login_usecase.dart
│   │   │           ├── register_usecase.dart
│   │   │           └── logout_usecase.dart
│   │   │
│   │   ├── home/                          # Home feature
│   │   │   ├── presentation/
│   │   │   │   ├── pages/
│   │   │   │   │   └── home_page.dart
│   │   │   │   ├── widgets/
│   │   │   │   │   ├── featured_languages.dart
│   │   │   │   │   ├── trending_topics.dart
│   │   │   │   │   ├── learning_stats_card.dart
│   │   │   │   │   └── quick_actions.dart
│   │   │   │   └── providers/
│   │   │   │       └── home_state_provider.dart
│   │   │   └── domain/
│   │   │       └── usecases/
│   │   │           └── get_dashboard_data_usecase.dart
│   │   │
│   │   ├── browse/                        # Browse languages feature
│   │   │   ├── presentation/
│   │   │   │   ├── pages/
│   │   │   │   │   ├── browse_page.dart
│   │   │   │   │   ├── language_detail_page.dart
│   │   │   │   │   └── category_page.dart
│   │   │   │   ├── widgets/
│   │   │   │   │   ├── language_card.dart
│   │   │   │   │   ├── language_grid.dart
│   │   │   │   │   ├── category_filter.dart
│   │   │   │   │   └── sort_dropdown.dart
│   │   │   │   └── providers/
│   │   │   │       ├── browse_provider.dart
│   │   │   │       └── language_detail_provider.dart
│   │   │   └── domain/
│   │   │       └── usecases/
│   │   │           ├── get_languages_usecase.dart
│   │   │           └── get_language_detail_usecase.dart
│   │   │
│   │   ├── learning_path/                 # Learning path feature
│   │   │   ├── presentation/
│   │   │   │   ├── pages/
│   │   │   │   │   ├── path_selection_page.dart
│   │   │   │   │   ├── path_overview_page.dart
│   │   │   │   │   ├── section_detail_page.dart
│   │   │   │   │   └── checkpoint_quiz_page.dart
│   │   │   │   ├── widgets/
│   │   │   │   │   ├── path_type_card.dart      # Quick vs Deep
│   │   │   │   │   ├── progress_indicator.dart
│   │   │   │   │   ├── section_list_item.dart
│   │   │   │   │   ├── section_card.dart
│   │   │   │   │   ├── code_example_widget.dart
│   │   │   │   │   ├── practice_problems_list.dart
│   │   │   │   │   ├── video_recommendations.dart
│   │   │   │   │   └── navigation_buttons.dart
│   │   │   │   └── providers/
│   │   │   │       ├── learning_path_provider.dart
│   │   │   │       ├── section_detail_provider.dart
│   │   │   │       └── quiz_provider.dart
│   │   │   └── domain/
│   │   │       └── usecases/
│   │   │           ├── create_path_usecase.dart
│   │   │           ├── get_section_usecase.dart
│   │   │           └── mark_complete_usecase.dart
│   │   │
│   │   ├── dashboard/                     # User dashboard feature
│   │   │   ├── presentation/
│   │   │   │   ├── pages/
│   │   │   │   │   └── dashboard_page.dart
│   │   │   │   ├── widgets/
│   │   │   │   │   ├── progress_chart.dart
│   │   │   │   │   ├── streak_calendar.dart
│   │   │   │   │   ├── recent_activity.dart
│   │   │   │   │   ├── achievements_grid.dart
│   │   │   │   │   └── stats_overview.dart
│   │   │   │   └── providers/
│   │   │   │       └── dashboard_provider.dart
│   │   │   └── domain/
│   │   │       └── usecases/
│   │   │           └── get_user_stats_usecase.dart
│   │   │
│   │   ├── search/                        # Search feature
│   │   │   ├── presentation/
│   │   │   │   ├── pages/
│   │   │   │   │   └── search_page.dart
│   │   │   │   ├── widgets/
│   │   │   │   │   ├── search_bar_widget.dart
│   │   │   │   │   ├── search_filters.dart
│   │   │   │   │   ├── search_result_card.dart
│   │   │   │   │   └── recent_searches.dart
│   │   │   │   └── providers/
│   │   │   │       └── search_provider.dart
│   │   │   └── domain/
│   │   │       └── usecases/
│   │   │           └── search_content_usecase.dart
│   │   │
│   │   ├── bookmarks/                     # Bookmarks feature
│   │   │   ├── presentation/
│   │   │   │   ├── pages/
│   │   │   │   │   └── bookmarks_page.dart
│   │   │   │   ├── widgets/
│   │   │   │   │