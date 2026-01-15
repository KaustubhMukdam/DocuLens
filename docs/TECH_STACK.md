# 💻 DocuLens - Technology Stack

Complete overview of all technologies, frameworks, libraries, and services used in DocuLens.

---

## Table of Contents

1. [Backend Stack](#backend-stack)
2. [Frontend Stack](#frontend-stack)
3. [Database & Storage](#database--storage)
4. [DevOps & Infrastructure](#devops--infrastructure)
5. [Third-Party Services](#third-party-services)
6. [Development Tools](#development-tools)
7. [Cost Estimation](#cost-estimation)

---

## Backend Stack

### Core Framework

#### FastAPI 0.109.0
```python
# Why FastAPI?
- High performance (on par with NodeJS and Go)
- Automatic API documentation (Swagger/OpenAPI)
- Built-in data validation (Pydantic)
- Async/await support
- Type hints for better IDE support
- Active community and development
```

**Installation:**
```bash
pip install fastapi[all]==0.109.0
```

**Key Features Used:**
- Path operations with type hints
- Dependency injection
- Background tasks
- WebSocket support (future)
- Request validation
- Response models

---

### Python Ecosystem

#### Python 3.11+
**Why This Version:**
- 25% faster than Python 3.10
- Better error messages
- Type hints improvements
- Task groups (async)
- TOML support in stdlib

**Standard Libraries Used:**
- `asyncio` - Async operations
- `typing` - Type hints
- `pathlib` - File operations
- `datetime` - Time handling
- `json` - JSON processing
- `hashlib` - Password hashing
- `secrets` - Token generation

---

### Database & ORM

#### PostgreSQL 15+
```yaml
Purpose: Primary relational database
Why PostgreSQL:
  - ACID compliant
  - JSON support (JSONB)
  - Full-text search
  - Advanced indexing
  - Proven scalability
  - Strong community

Features Used:
  - Foreign keys & constraints
  - Indexes (B-tree, GIN, GIST)
  - Triggers for automation
  - Views for complex queries
  - Partitioning for large tables
```

#### SQLAlchemy 2.0+
```python
Purpose: ORM (Object-Relational Mapping)

Features:
  - Async support (asyncpg driver)
  - Migration support via Alembic
  - Connection pooling
  - Relationship loading strategies
  - Query optimization

# Example Model
class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
```

#### Alembic 1.13+
```python
Purpose: Database migrations

# Create migration
alembic revision --autogenerate -m "add_users_table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

### Caching & Session Storage

#### Redis 7.2
```yaml
Purpose: Caching, session storage, rate limiting

Use Cases:
  - Cache API responses (TTL: 5-60 minutes)
  - Store user sessions
  - Rate limiting counters
  - Real-time data (active users)
  - Pub/Sub for notifications

Data Structures Used:
  - Strings: Simple key-value
  - Hashes: User sessions
  - Sets: Unique items (user IDs)
  - Sorted Sets: Leaderboards
  - Lists: Recent activity
```

**Python Client:**
```python
# redis-py 5.0+
import redis.asyncio as redis

redis_client = redis.from_url(
    "redis://localhost:6379",
    encoding="utf-8",
    decode_responses=True
)

# Cache example
await redis_client.setex("user:123", 3600, json.dumps(user_data))
```

---

### AI & Machine Learning

#### Anthropic Claude API
```python
Purpose: AI-powered summarization

Model: claude-sonnet-4-20250514

Capabilities:
  - 200K token context window
  - Excellent summarization quality
  - Source attribution
  - Consistent output

Pricing:
  - Input: $3 per 1M tokens
  - Output: $15 per 1M tokens

# Usage Example
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=[{
        "role": "user",
        "content": "Summarize this documentation..."
    }]
)
```

#### Sentence Transformers (Optional)
```python
Purpose: Generate embeddings for semantic search

Model: all-MiniLM-L6-v2
Dimensions: 384
Cost: Free (self-hosted)

# Installation
pip install sentence-transformers

# Usage
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(texts)
```

---

### Web Scraping

#### BeautifulSoup4 4.12+
```python
Purpose: HTML parsing

from bs4 import BeautifulSoup

soup = BeautifulSoup(html_content, 'html.parser')
headings = soup.find_all(['h1', 'h2', 'h3'])
code_blocks = soup.find_all('code')
```

#### Scrapy 2.11+
```python
Purpose: Large-scale web scraping

Features:
  - Asynchronous requests
  - Built-in middleware
  - Item pipelines
  - Export to JSON/CSV
  - Robots.txt compliance

# Basic Spider
class PythonDocsSpider(scrapy.Spider):
    name = 'python_docs'
    start_urls = ['https://docs.python.org/3/']
    
    def parse(self, response):
        # Extract data
        pass
```

#### Playwright 1.40+
```python
Purpose: Browser automation for JavaScript-heavy sites

from playwright.async_api import async_playwright

async with async_playwright() as p:
    browser = await p.chromium.launch()
    page = await browser.new_page()
    await page.goto('https://docs.flutter.dev/')
    content = await page.content()
```

#### Requests 2.31+
```python
Purpose: Simple HTTP requests

import requests

response = requests.get(
    'https://api.github.com/repos/python/cpython',
    headers={'Authorization': f'token {github_token}'}
)
```

---

### Task Queue

#### Celery 5.3+
```python
Purpose: Distributed task queue

Broker: RabbitMQ or Redis

Use Cases:
  - Scheduled scraping jobs
  - AI summarization (async)
  - Email sending
  - Data cleanup tasks

# Task Definition
@celery_app.task
def scrape_documentation(language_id: str):
    # Scraping logic
    pass

# Schedule Task
scrape_documentation.apply_async(
    args=[language_id],
    countdown=60  # Run after 60 seconds
)
```

#### RabbitMQ 3.12
```yaml
Purpose: Message broker for Celery

Why RabbitMQ:
  - Reliable message delivery
  - Flexible routing
  - Dead letter queues
  - Message persistence
  - Easy monitoring

Alternative: Redis (simpler setup)
```

---

### Authentication & Security

#### PyJWT 2.8+
```python
Purpose: JWT token generation and validation

from jose import jwt
from datetime import datetime, timedelta

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
```

#### Passlib 1.7+
```python
Purpose: Password hashing

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
hashed = pwd_context.hash("user_password")

# Verify password
pwd_context.verify("user_password", hashed)
```

#### Python-Multipart
```python
Purpose: Form data and file uploads

pip install python-multipart

# FastAPI automatically uses this for forms
```

---

### Testing

#### Pytest 7.4+
```python
Purpose: Testing framework

# Installation
pip install pytest pytest-asyncio pytest-cov

# Test Example
def test_create_user(client):
    response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "Test123!"
    })
    assert response.status_code == 201
```

#### Faker 22.0+
```python
Purpose: Generate test data

from faker import Faker
fake = Faker()

test_user = {
    "email": fake.email(),
    "name": fake.name(),
    "username": fake.user_name()
}
```

#### Factory Boy 3.3+
```python
Purpose: Test fixtures

import factory

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    email = factory.Faker('email')
    username = factory.Faker('user_name')
```

---

### Code Quality

#### Black 23.12+
```python
Purpose: Code formatting

# Format all files
black .

# Check only
black --check .

# Config in pyproject.toml
[tool.black]
line-length = 100
target-version = ['py311']
```

#### Ruff 0.1+
```python
Purpose: Fast Python linter (replaces Flake8, isort, etc.)

# Lint all files
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Config in pyproject.toml
[tool.ruff]
line-length = 100
select = ["E", "F", "I"]
```

#### MyPy 1.8+
```python
Purpose: Static type checking

# Check types
mypy app/

# Config in mypy.ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
```

#### Pre-commit
```yaml
Purpose: Git hooks for code quality

# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
  
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
```

---

### Monitoring & Logging

#### Loguru
```python
Purpose: Enhanced logging

from loguru import logger

logger.add(
    "logs/app.log",
    rotation="1 day",
    retention="1 month",
    level="INFO"
)

logger.info("User {user_id} logged in", user_id=user.id)
logger.error("Failed to scrape {url}", url=doc_url)
```

#### Sentry
```python
Purpose: Error tracking and monitoring

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1
)
```

---

### Additional Backend Libraries

```python
# Email
python-jose==3.3.0          # JWT tokens
python-multipart==0.0.6     # Form uploads
email-validator==2.1.0      # Email validation

# HTTP
httpx==0.26.0               # Async HTTP client
aiofiles==23.2.1            # Async file operations

# Utilities
python-dotenv==1.0.0        # Environment variables
pydantic-settings==2.1.0    # Settings management
tenacity==8.2.3             # Retry logic
```

---

## Frontend Stack

### Core Framework

#### Flutter 3.22+ (Stable)
```yaml
Why Flutter:
  - Single codebase for Web, iOS, Android
  - High performance (60+ FPS)
  - Rich widget library
  - Hot reload for fast development
  - Google backing and strong community

Platforms:
  - iOS: 14+
  - Android: API 26+ (Android 8.0)
  - Web: All modern browsers
  - Desktop: Windows, macOS, Linux (future)
```

**Installation:**
```bash
# Install Flutter SDK
git clone https://github.com/flutter/flutter.git -b stable
export PATH="$PATH:`pwd`/flutter/bin"

# Verify installation
flutter doctor
```

---

### State Management

#### Riverpod 2.4+
```dart
Purpose: State management solution

Why Riverpod:
  - Compile-safe
  - Testable
  - No BuildContext needed
  - Provider generator
  - Async support

// Provider Example
@riverpod
Future<User> currentUser(CurrentUserRef ref) async {
  final token = await ref.watch(authTokenProvider.future);
  return api.getCurrentUser(token);
}

// Consumer Example
Consumer(
  builder: (context, ref, child) {
    final user = ref.watch(currentUserProvider);
    return user.when(
      data: (user) => Text('Hello ${user.name}'),
      loading: () => CircularProgressIndicator(),
      error: (err, stack) => Text('Error: $err'),
    );
  },
)
```

**Alternative:** Bloc Pattern (if team prefers)

---

### Networking

#### Dio 5.4+
```dart
Purpose: Advanced HTTP client

Features:
  - Interceptors
  - Request cancellation
  - File download/upload
  - FormData support
  - Automatic retries

// Dio Setup
final dio = Dio(BaseOptions(
  baseUrl: 'https://api.doculens.dev',
  connectTimeout: Duration(seconds: 30),
  receiveTimeout: Duration(seconds: 30),
));

// Add interceptors
dio.interceptors.add(AuthInterceptor());
dio.interceptors.add(LogInterceptor());

// Make request
final response = await dio.get('/api/v1/languages');
```

#### Retrofit 4.0+
```dart
Purpose: Type-safe API client generation

// API Definition
@RestApi(baseUrl: "https://api.doculens.dev")
abstract class ApiClient {
  factory ApiClient(Dio dio, {String baseUrl}) = _ApiClient;
  
  @GET("/api/v1/languages")
  Future<List<Language>> getLanguages();
  
  @POST("/api/v1/auth/login")
  Future<AuthResponse> login(@Body() LoginRequest request);
}

// Usage
final client = ApiClient(dio);
final languages = await client.getLanguages();
```

---

### Local Storage

#### Hive 2.2+
```dart
Purpose: Fast, NoSQL database

Why Hive:
  - Pure Dart (no native dependencies)
  - Fast (faster than SQLite for small data)
  - Lazy box loading
  - Encryption support
  - Type adapters

// Initialize
await Hive.initFlutter();
Hive.registerAdapter(UserAdapter());

// Open box
final box = await Hive.openBox<User>('users');

// CRUD operations
await box.put('current', user);
final user = box.get('current');
await box.delete('current');
```

#### Shared Preferences
```dart
Purpose: Simple key-value storage

final prefs = await SharedPreferences.getInstance();

// Store
await prefs.setString('theme', 'dark');
await prefs.setBool('onboarding_complete', true);

// Retrieve
final theme = prefs.getString('theme') ?? 'light';
final onboarded = prefs.getBool('onboarding_complete') ?? false;
```

#### Sqflite (Optional)
```dart
Purpose: SQLite for complex queries

// Only if needed for advanced features
final db = await openDatabase('doculens.db');
await db.execute('''
  CREATE TABLE progress(
    id INTEGER PRIMARY KEY,
    section_id TEXT,
    completed INTEGER
  )
''');
```

---

### UI Components & Styling

#### Material Design 3
```dart
Purpose: Modern Material Design components

// Theme
ThemeData(
  colorScheme: ColorScheme.fromSeed(
    seedColor: Color(0xFF6366F1),
    brightness: Brightness.light,
  ),
  useMaterial3: true,
)

// Components used
- AppBar
- BottomNavigationBar
- Card
- Chip
- Dialog
- FloatingActionButton
- TextField
- etc.
```

#### Google Fonts
```dart
Purpose: Custom typography

import 'package:google_fonts/google_fonts.dart';

TextTheme textTheme = GoogleFonts.interTextTheme();
TextTheme headingTheme = GoogleFonts.plusJakartaSansTextTheme();
TextTheme codeTheme = GoogleFonts.jetBrainsMonoTextTheme();
```

---

### Code Display & Markdown

#### Flutter Markdown 0.6+
```dart
Purpose: Render documentation

import 'package:flutter_markdown/flutter_markdown.dart';

Markdown(
  data: docContent,
  styleSheet: MarkdownStyleSheet(
    code: TextStyle(
      fontFamily: 'JetBrains Mono',
      backgroundColor: Colors.grey.shade200,
    ),
  ),
  onTapLink: (text, href, title) {
    // Handle link taps
  },
)
```

#### Syntax Highlighter
```dart
Purpose: Code syntax highlighting

import 'package:flutter_highlight/flutter_highlight.dart';
import 'package:flutter_highlight/themes/github.dart';

HighlightView(
  code,
  language: 'python',
  theme: githubTheme,
  padding: EdgeInsets.all(12),
  textStyle: TextStyle(fontFamily: 'JetBrains Mono'),
)
```

---

### Navigation

#### Go Router 13.0+
```dart
Purpose: Declarative routing

Why Go Router:
  - Deep linking support
  - Type-safe routes
  - Nested navigation
  - Redirect logic
  - Query parameters

// Router configuration
final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => HomePage(),
    ),
    GoRoute(
      path: '/language/:slug',
      builder: (context, state) {
        final slug = state.pathParameters['slug']!;
        return LanguagePage(slug: slug);
      },
    ),
    GoRoute(
      path: '/learning-path/:id',
      builder: (context, state) => LearningPathPage(
        id: state.pathParameters['id']!,
      ),
    ),
  ],
);

// Navigation
context.go('/language/python');
context.push('/learning-path/123');
```

---

### Authentication

#### Flutter Secure Storage
```dart
Purpose: Secure token storage

import 'package:flutter_secure_storage/flutter_secure_storage.dart';

final storage = FlutterSecureStorage();

// Store tokens
await storage.write(key: 'access_token', value: token);
await storage.write(key: 'refresh_token', value: refreshToken);

// Retrieve
final token = await storage.read(key: 'access_token');

// Delete
await storage.delete(key: 'access_token');
```

#### Google Sign-In
```dart
Purpose: OAuth with Google

import 'package:google_sign_in/google_sign_in.dart';

final GoogleSignIn googleSignIn = GoogleSignIn(
  scopes: ['email', 'profile'],
);

// Sign in
final account = await googleSignIn.signIn();
final auth = await account?.authentication;
```

---

### Animations

#### Lottie 3.0+
```dart
Purpose: High-quality animations

import 'package:lottie/lottie.dart';

Lottie.asset(
  'assets/animations/loading.json',
  width: 200,
  height: 200,
)
```

#### Built-in Animations
```dart
// Hero animation
Hero(
  tag: 'language-logo',
  child: Image.network(logoUrl),
)

// Animated Container
AnimatedContainer(
  duration: Duration(milliseconds: 300),
  curve: Curves.easeInOut,
  color: isSelected ? primaryColor : Colors.white,
)

// Page transitions
PageRouteBuilder(
  transitionDuration: Duration(milliseconds: 300),
  pageBuilder: (context, animation, secondaryAnimation) => NextPage(),
  transitionsBuilder: (context, animation, secondaryAnimation, child) {
    return FadeTransition(opacity: animation, child: child);
  },
)
```

---

### Charts & Visualizations

#### FL Chart 0.66+
```dart
Purpose: Beautiful charts for analytics

import 'package:fl_chart/fl_chart.dart';

// Line chart for progress
LineChart(
  LineChartData(
    lineBarsData: [
      LineChartBarData(
        spots: progressData,
        isCurved: true,
        color: primaryColor,
      ),
    ],
  ),
)

// Bar chart for statistics
BarChart(
  BarChartData(
    barGroups: statsData,
  ),
)
```

---

### Testing

#### Flutter Test
```dart
Purpose: Unit and widget testing

// Widget test
testWidgets('Login button triggers login', (tester) async {
  await tester.pumpWidget(MyApp());
  
  await tester.enterText(
    find.byType(TextField).first,
    'test@example.com',
  );
  
  await tester.tap(find.text('Login'));
  await tester.pumpAndSettle();
  
  expect(find.text('Welcome'), findsOneWidget);
});
```

#### Integration Test
```dart
Purpose: End-to-end testing

// integration_test/app_test.dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();
  
  testWidgets('Complete user journey', (tester) async {
    app.main();
    await tester.pumpAndSettle();
    
    // Test complete user flow
  });
}
```

#### Mockito 5.4+
```dart
Purpose: Mocking dependencies

@GenerateMocks([ApiClient, AuthService])
void main() {
  late MockApiClient mockApi;
  
  setUp(() {
    mockApi = MockApiClient();
  });
  
  test('Fetches languages successfully', () async {
    when(mockApi.getLanguages())
        .thenAnswer((_) async => [pythonLanguage]);
    
    final result = await repository.getLanguages();
    expect(result, [pythonLanguage]);
  });
}
```

---

### Code Quality

#### Flutter Analyze
```dart
Purpose: Static analysis

# Run analysis
flutter analyze

# analysis_options.yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  strong-mode:
    implicit-casts: false
    implicit-dynamic: false

linter:
  rules:
    - prefer_const_constructors
    - avoid_print
    - prefer_single_quotes
```

---

### Additional Flutter Packages

```yaml
# pubspec.yaml

dependencies:
  # Core
  flutter:
    sdk: flutter
  
  # State Management
  flutter_riverpod: ^2.4.9
  riverpod_annotation: ^2.3.3
  
  # Networking
  dio: ^5.4.0
  retrofit: ^4.0.3
  
  # Storage
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  shared_preferences: ^2.2.2
  flutter_secure_storage: ^9.0.0
  
  # UI
  google_fonts: ^6.1.0
  flutter_markdown: ^0.6.18
  flutter_highlight: ^0.7.0
  lottie: ^3.0.0
  fl_chart: ^0.66.0
  
  # Navigation
  go_router: ^13.0.0
  
  # Authentication
  google_sign_in: ^6.2.1
  
  # Utilities
  intl: ^0.19.0
  url_launcher: ^6.2.3
  share_plus: ^7.2.1
  path_provider: ^2.1.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  
  # Code Generation
  build_runner: ^2.4.7
  riverpod_generator: ^2.3.9
  retrofit_generator: ^8.0.6
  hive_generator: ^2.0.1
  
  # Testing
  mockito: ^5.4.4
  integration_test:
    sdk: flutter
  
  # Linting
  flutter_lints: ^3.0.1
```

---

## Database & Storage

### PostgreSQL Configuration

```yaml
Version: 15+

Configuration (postgresql.conf):
  max_connections: 200
  shared_buffers: 256MB
  effective_cache_size: 1GB
  maintenance_work_mem: 64MB
  checkpoint_completion_target: 0.9
  wal_buffers: 16MB
  default_statistics_target: 100
  random_page_cost: 1.1
  effective_io_concurrency: 200
  work_mem: 655kB
  min_wal_size: 1GB
  max_wal_size: 4GB

Extensions:
  - uuid-ossp (UUID generation)
  - pg_trgm (Fuzzy text search)
  - btree_gin (Better indexing)
```

### Redis Configuration

```conf
# redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
appendonly yes
appendfsync everysec
```

---

## DevOps & Infrastructure

### Containerization

#### Docker 24.0+
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/doculens
      - REDIS_URL=redis://redis:6379
  
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: doculens
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend

volumes:
  postgres_data:
  redis_data:
```

---

### CI/CD

#### GitHub Actions
```yaml
# .github/workflows/backend-ci.yml
name: Backend CI

on:
  push:
    branches: [main, develop]
    paths:
      - 'backend/**'
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run linting
        run: |
          cd backend
          ruff check .
          black --check .
      
      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml

```

```yaml
# .github/workflows/frontend-ci.yml
name: Frontend CI

on:
  push:
    branches: [main, develop]
    paths:
      - 'frontend/**'

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.22.0'
      
      - name: Install dependencies
        run: |
          cd frontend
          flutter pub get
      
      - name: Run analyzer
        run: |
          cd frontend
          flutter analyze
      
      - name: Run tests
        run: |
          cd frontend
          flutter test --coverage
      
      - name: Build APK
        run: |
          cd frontend
          flutter build apk --release
```

---

### Cloud Hosting (AWS)

```yaml
EC2 Instances:
  - Type: t3.medium (MVP), t3.large (production)
  - OS: Ubuntu 22.04 LTS
  - Auto Scaling Group
  - Application Load Balancer

RDS (PostgreSQL):
  - Instance: db.t3.medium
  - Multi-AZ for HA
  - Automated backups
  - Read replicas for scaling

ElastiCache (Redis):
  - Instance: cache.t3.medium
  - Redis 7.x
  - Cluster mode enabled

S3:
  - Bucket for static assets
  - Bucket for backups
  - Versioning enabled
  - Lifecycle policies

CloudFront:
  - CDN for static content
  - SSL/TLS certificates
  - Global edge locations

Route 53:
  - DNS management
  - Health checks
  - Failover routing
```

---

### Alternative: DigitalOcean

```yaml
Droplets:
  - Size: Basic ($24/mo) for MVP
  - Size: General Purpose ($80/mo) for production
  - Ubuntu 22.04

Managed Database:
  - PostgreSQL cluster
  - Automatic backups
  - Connection pooling

Spaces:
  - Object storage (S3-compatible)
  - CDN included
  - $5/mo for 250GB

App Platform:
  - Managed platform for containers
  - Auto-scaling
  - $12/mo starting
```

---

### Monitoring

#### Sentry
```yaml
Purpose: Error tracking

Features:
  - Error aggregation
  - Stack traces
  - Release tracking
  - Performance monitoring
  - User feedback

Pricing:
  - Free: 5K errors/month
  - Team: $26/month (50K errors)

Integration:
  - Python SDK for backend
  - Flutter SDK for mobile
```

#### Prometheus + Grafana
```yaml
Purpose: Metrics and visualization

Prometheus:
  - Time-series database
  - Service discovery
  - Alerting rules

Grafana:
  - Dashboard visualization
  - Multiple data sources
  - Alerting

Metrics Collected:
  - API response times
  - Database query times
  - Cache hit rates
  - Error rates
  - Active users
```

---

### Reverse Proxy & Load Balancing

#### Nginx 1.25+
```nginx
Purpose: Reverse proxy, load balancing, SSL termination

# Example nginx.conf
upstream backend {
    least_conn;
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    listen 443 ssl http2;
    server_name api.doculens.dev;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Let's Encrypt
```bash
Purpose: Free SSL certificates

# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d doculens.dev -d www.doculens.dev

# Auto-renewal (cron job)
0 0 * * * certbot renew --quiet
```

---

## Third-Party Services

### AI & LLM Services

#### Groq API (Primary)
```python
Purpose: Fast, cost-effective LLM inference

Why Groq:
  - 10x faster inference than traditional APIs
  - Lower latency (~500ms response)
  - Cost-effective pricing
  - Good for summarization tasks
  - Llama 3 models available

Models Available:
  - llama-3.1-70b-versatile (Primary for summarization)
  - llama-3.1-8b-instant (For quick tasks)
  - mixtral-8x7b-32768
  - gemma-7b-it

Pricing:
  - More cost-effective than OpenAI/Anthropic
  - Pay per token usage
  - Free tier available

Usage Example:
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a documentation summarizer. Provide concise summaries while maintaining accuracy."
        },
        {
            "role": "user",
            "content": f"Summarize this documentation: {doc_content}"
        }
    ],
    model="llama-3.1-70b-versatile",
    temperature=0.3,
    max_tokens=1000,
)

summary = chat_completion.choices[0].message.content
```

#### Anthropic Claude API (Backup/Premium)
```python
Purpose: High-quality summarization for premium features

Model: claude-sonnet-4-20250514

When to use:
  - Premium user requests
  - High-quality summaries needed
  - Groq API fails or rate limited
  - Complex technical documentation

Pricing:
  - Input: $3 per 1M tokens
  - Output: $15 per 1M tokens

# Fallback logic
try:
    # Try Groq first (faster, cheaper)
    summary = await groq_summarize(content)
except GroqAPIError:
    # Fallback to Claude for reliability
    summary = await claude_summarize(content)
```

---

### Video Platform

#### YouTube Data API v3
```python
Purpose: Video recommendations and metadata

Quota: 10,000 units/day (free)

from googleapiclient.discovery import build

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Search for videos
request = youtube.search().list(
    part="snippet",
    q="python tutorial variables",
    type="video",
    maxResults=5,
    relevanceLanguage="en",
    videoDuration="medium"  # 4-20 minutes
)

response = request.execute()
```

---

### Practice Platforms

#### LeetCode (Unofficial API)
```python
Purpose: Practice problem integration

Note: No official API, use with caution

# GraphQL endpoint
url = "https://leetcode.com/graphql"

query = """
query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
  problemsetQuestionList(
    categorySlug: $categorySlug
    limit: $limit
    skip: $skip
    filters: $filters
  ) {
    questions {
      title
      titleSlug
      difficulty
      topicTags {
        name
      }
    }
  }
}
"""

# Rate limiting recommended
```

#### HackerRank (Unofficial API)
```python
Purpose: Additional practice problems

# Similar approach - web scraping with rate limiting
# Consider caching results heavily
```

---

### Cloud Storage

#### AWS S3 / Cloudflare R2
```python
Purpose: Static assets, scraped content, backups

Why Cloudflare R2:
  - S3-compatible API
  - No egress fees
  - Cheaper than AWS S3
  - Good for serving static content

# boto3 client (works with both S3 and R2)
import boto3

s3_client = boto3.client(
    's3',
    endpoint_url='https://<account-id>.r2.cloudflarestorage.com',
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY
)

# Upload file
s3_client.upload_file('local_file.pdf', 'doculens-content', 'docs/file.pdf')
```

---

### CDN

#### Cloudflare
```yaml
Purpose: CDN, DDoS protection, analytics

Features:
  - Free tier available
  - Global edge network
  - SSL/TLS
  - Web Application Firewall (WAF)
  - Analytics
  - Page Rules
  - Workers for edge computing

Benefits:
  - Reduce server load
  - Faster content delivery
  - DDoS protection
  - Cost-effective
```

---

### Email Services

#### SendGrid / AWS SES
```python
Purpose: Transactional emails

SendGrid (Recommended for MVP):
  - Free: 100 emails/day
  - Essentials: $19.95/month (50K emails)
  - Easy setup
  - Good deliverability

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='noreply@doculens.dev',
    to_emails='user@example.com',
    subject='Welcome to DocuLens',
    html_content='<strong>Welcome!</strong>'
)

sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
response = sg.send(message)

AWS SES (For production scale):
  - $0.10 per 1,000 emails
  - Better for high volume
  - Requires domain verification
```

---

### Authentication Providers

#### Google OAuth
```python
Purpose: Social login

# Python backend
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)
```

#### GitHub OAuth
```dart
Purpose: Developer-friendly auth

// Flutter implementation
import 'package:flutter_web_auth/flutter_web_auth.dart';

final result = await FlutterWebAuth.authenticate(
  url: 'https://github.com/login/oauth/authorize?client_id=$clientId',
  callbackUrlScheme: 'doculens',
);
```

---

### Analytics

#### Google Analytics 4
```javascript
Purpose: User behavior tracking

Features:
  - Free tier
  - Event-based tracking
  - User segmentation
  - Conversion tracking
  - Cross-platform tracking

// Web integration
gtag('event', 'section_completed', {
  'language': 'python',
  'section_id': 'variables',
  'path_type': 'quick'
});
```

#### Mixpanel (Optional)
```python
Purpose: Product analytics

Features:
  - Free: 100K events/month
  - Funnel analysis
  - Retention analysis
  - A/B testing
  - User profiles

from mixpanel import Mixpanel

mp = Mixpanel(MIXPANEL_TOKEN)

mp.track(user_id, 'Section Completed', {
    'language': 'python',
    'section': 'variables',
    'time_spent': 320
})
```

---

## Development Tools

### Version Control

#### Git & GitHub
```bash
# Repository structure
https://github.com/KaustubhMukdam/DocuLens.git

Branches:
  - main (production)
  - develop (development)
  - feature/* (new features)
  - bugfix/* (bug fixes)
  - hotfix/* (urgent fixes)

# Git workflow
git checkout develop
git checkout -b feature/add-search
# ... make changes ...
git add .
git commit -m "feat: add semantic search functionality"
git push origin feature/add-search
# Create PR to develop
```

---

### IDEs & Editors

#### Visual Studio Code
```json
Purpose: Primary IDE

Extensions:
  - Python (Microsoft)
  - Pylance (Type checking)
  - Flutter
  - Dart
  - GitLens
  - Docker
  - REST Client
  - Thunder Client
  - Better Comments
  - Error Lens

// .vscode/settings.json
{
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  },
  "[dart]": {
    "editor.formatOnSave": true,
    "editor.rulers": [80]
  }
}
```

#### Android Studio
```yaml
Purpose: Flutter development, Android emulators

Features:
  - Flutter plugin
  - Dart plugin
  - Android emulators
  - Device debugging
  - Performance profiling
```

#### PyCharm Professional (Optional)
```yaml
Purpose: Advanced Python development

Features:
  - Database tools
  - Advanced debugging
  - Code analysis
  - Refactoring tools
  - Remote development

Note: VSCode is sufficient for MVP
```

---

### API Testing

#### Postman / Insomnia
```yaml
Purpose: API testing and documentation

Features:
  - Request collections
  - Environment variables
  - Test scripts
  - Mock servers
  - API documentation

# Alternative: Thunder Client (VSCode extension)
```

---

### Database Management

#### pgAdmin 4 / DBeaver
```yaml
Purpose: PostgreSQL GUI

pgAdmin:
  - Official PostgreSQL tool
  - Query tool
  - Schema visualization
  - Backup/restore

DBeaver:
  - Multi-database support
  - SQL editor
  - ER diagrams
  - Data export/import
```

#### RedisInsight
```yaml
Purpose: Redis GUI

Features:
  - Key browser
  - CLI
  - Profiler
  - Slow log
  - Memory analysis
```

---

### Design Tools

#### Figma
```yaml
Purpose: UI/UX design

Features:
  - Collaborative design
  - Prototyping
  - Component libraries
  - Design systems
  - Developer handoff

Plan: Free tier sufficient
```

#### Excalidraw
```yaml
Purpose: Quick diagrams and wireframes

Features:
  - Hand-drawn style
  - Collaborative
  - Free and open-source
  - Export to PNG/SVG
```

---

### Project Management

#### GitHub Projects
```yaml
Purpose: Integrated project management

Features:
  - Kanban boards
  - Issue tracking
  - Milestones
  - Project roadmaps
  - Automation

Boards:
  - Backlog
  - To Do
  - In Progress
  - In Review
  - Done
```

#### Notion (Optional)
```yaml
Purpose: Documentation and notes

Use Cases:
  - Meeting notes
  - Design decisions
  - Research
  - Knowledge base
```

---

## Cost Estimation

### Development Phase (Months 1-3)

```yaml
One-Time Costs:
  Domain (doculens.dev): $12/year
  Design (Figma, assets): $500
  SSL Certificate: $0 (Let's Encrypt)
  TOTAL: $512

Monthly Costs:
  Hosting (DigitalOcean Droplet): $0 (Free tier / $6 basic)
  Database: $0 (Free tier / Included)
  Redis: $0 (Free tier / Included)
  Groq API: $50 (development usage)
  Claude API: $0 (minimal backup usage)
  YouTube API: $0 (Free)
  SendGrid: $0 (Free 100 emails/day)
  Cloudflare: $0 (Free tier)
  TOTAL: ~$50/month

Total Development Budget: $662
```

### Production - First 1,000 Users (Months 4-6)

```yaml
Monthly Costs:
  Hosting (DigitalOcean):
    - Droplet (2GB RAM): $18
    - Database (1GB): $15
    - Total: $33
  
  OR AWS:
    - EC2 t3.small: $15
    - RDS db.t3.micro: $16
    - ElastiCache t3.micro: $12
    - Total: $43
  
  AI APIs:
    - Groq API: $100 (primary)
    - Claude API: $50 (backup/premium)
    - Total: $150
  
  Storage & CDN:
    - Cloudflare R2: $10
    - Cloudflare CDN: $0 (Free)
    - Total: $10
  
  Services:
    - SendGrid: $0 (Free tier)
    - Sentry: $0 (Free tier)
    - Analytics: $0 (Free tier)
    - Total: $0
  
  TOTAL: $193/month (DigitalOcean) or $203/month (AWS)
```

### Production - 10,000 Users (Months 7-12)

```yaml
Monthly Costs:
  Hosting (DigitalOcean):
    - Droplets (2x 4GB): $96
    - Load Balancer: $12
    - Database (4GB): $60
    - Managed Redis: $30
    - Total: $198
  
  OR AWS:
    - EC2 (2x t3.medium): $60
    - RDS (db.t3.small): $30
    - ElastiCache (cache.t3.small): $24
    - ALB: $23
    - Total: $137
  
  AI APIs:
    - Groq API: $400 (increased usage)
    - Claude API: $200 (premium users)
    - Total: $600
  
  Storage & CDN:
    - Cloudflare R2: $30
    - Cloudflare Pro: $20 (optional)
    - Total: $50
  
  Services:
    - SendGrid: $20 (Essentials plan)
    - Sentry: $26 (Team plan)
    - Monitoring: $20 (Grafana Cloud)
    - Total: $66
  
  TOTAL: $914/month (AWS - recommended for scale)
```

### Production - 50,000 Users (Year 2)

```yaml
Monthly Costs:
  Hosting (AWS):
    - EC2 (4x t3.large): $240
    - RDS (db.r5.large): $145
    - ElastiCache cluster: $100
    - ALB: $23
    - Total: $508
  
  AI APIs:
    - Groq API: $1,500
    - Claude API: $500
    - Total: $2,000
  
  Storage & CDN:
    - S3/R2: $100
    - CloudFront/Cloudflare: $50
    - Total: $150
  
  Services:
    - SendGrid: $90 (Pro plan)
    - Sentry: $99
    - Monitoring: $50
    - Backups: $30
    - Total: $269
  
  TOTAL: $2,927/month
```

---

## Cost Optimization Strategies

### 1. AI API Costs
```python
Strategies:
  1. Aggressive caching (Redis)
     - Cache summaries for 30+ days
     - Save ~70% on API calls
  
  2. Use Groq for 90% of requests
     - 10x cheaper than Claude
     - Reserve Claude for premium/complex docs
  
  3. Batch processing
     - Summarize during low-traffic hours
     - Use async workers
  
  4. Smart summarization
     - Only re-summarize if content changed >10%
     - Version control for summaries
  
  Savings: $500-1000/month at 10K users
```

### 2. Infrastructure Costs
```yaml
Strategies:
  1. Reserved Instances (AWS)
     - 1-year: 30% savings
     - 3-year: 50% savings
  
  2. Spot Instances for workers
     - 70-90% cheaper
     - Use for scraping jobs
  
  3. Auto-scaling
     - Scale down during low traffic
     - Save 30-40% on compute
  
  4. Database optimization
     - Connection pooling
     - Read replicas only when needed
     - Efficient queries
  
  Savings: $200-400/month at 10K users
```

### 3. Storage Costs
```yaml
Strategies:
  1. Cloudflare R2 vs AWS S3
     - No egress fees
     - Save ~70% on storage costs
  
  2. Intelligent tiering
     - Hot: Recent content (SSD)
     - Warm: Older content (Standard)
     - Cold: Archives (Glacier)
  
  3. Compression
     - Gzip for text content
     - WebP for images
     - Save 60-80% on bandwidth
  
  Savings: $50-100/month at 10K users
```

---

## Tech Stack Summary

### Backend
- **Framework**: FastAPI 0.109.0
- **Language**: Python 3.11+
- **Database**: PostgreSQL 15+
- **Cache**: Redis 7.2
- **ORM**: SQLAlchemy 2.0+
- **Migrations**: Alembic 1.13+
- **Task Queue**: Celery 5.3+ + RabbitMQ 3.12
- **AI**: Groq API (Primary), Claude API (Backup)
- **Scraping**: BeautifulSoup4, Scrapy, Playwright
- **Testing**: Pytest 7.4+
- **Code Quality**: Black, Ruff, MyPy

### Frontend
- **Framework**: Flutter 3.22+
- **Language**: Dart 3.4+
- **State Management**: Riverpod 2.4+
- **Networking**: Dio 5.4+ + Retrofit 4.0+
- **Storage**: Hive 2.2+ + SharedPreferences
- **Navigation**: GoRouter 13.0+
- **Testing**: Flutter Test + Mockito

### DevOps
- **Containers**: Docker 24.0+ + Docker Compose
- **CI/CD**: GitHub Actions
- **Hosting**: AWS / DigitalOcean
- **CDN**: Cloudflare
- **Monitoring**: Sentry + Prometheus + Grafana
- **SSL**: Let's Encrypt

### Third-Party
- **AI**: Groq API (Primary), Anthropic Claude (Backup)
- **Video**: YouTube Data API v3
- **Email**: SendGrid / AWS SES
- **Auth**: Google OAuth, GitHub OAuth
- **Analytics**: Google Analytics 4
- **Storage**: AWS S3 / Cloudflare R2

---

## Migration from Claude to Groq

### Why Groq?
```yaml
Performance:
  - 10x faster inference
  - ~500ms response time
  - Real-time summarization possible

Cost:
  - Significantly cheaper than Claude/GPT-4
  - Better for high-volume usage
  - More sustainable for freemium model

Quality:
  - Llama 3.1 70B performs well
  - Good for summarization tasks
  - Acceptable trade-off for cost savings

Strategy:
  - Use Groq for 90% of requests
  - Fallback to Claude for failures
  - Claude for premium features
```

### Implementation
```python
# services/ai_service.py

class AIService:
    def __init__(self):
        self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
        self.claude_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async def summarize(
        self, 
        content: str, 
        use_premium: bool = False
    ) -> str:
        """
        Summarize documentation content.
        
        Args:
            content: Documentation content to summarize
            use_premium: Use Claude API for higher quality
        
        Returns:
            Summarized content with source attribution
        """
        if use_premium:
            return await self._claude_summarize(content)
        
        try:
            # Try Groq first (faster, cheaper)
            return await self._groq_summarize(content)
        except GroqAPIError as e:
            logger.warning(f"Groq API failed: {e}, falling back to Claude")
            # Fallback to Claude
            return await self._claude_summarize(content)
    
    async def _groq_summarize(self, content: str) -> str:
        """Summarize using Groq API"""
        chat_completion = await self.groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """You are a technical documentation summarizer.
                    Create concise summaries while maintaining accuracy.
                    Always mention the source and key concepts."""
                },
                {
                    "role": "user",
                    "content": f"Summarize this documentation:\n\n{content}"
                }
            ],
            model="llama-3.1-70b-versatile",
            temperature=0.3,
            max_tokens=1000,
        )
        
        return chat_completion.choices[0].message.content
    
    async def _claude_summarize(self, content: str) -> str:
        """Summarize using Claude API (backup/premium)"""
        message = await self.claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"Summarize this documentation:\n\n{content}"
            }]
        )
        
        return message.content[0].text
```

---

**Tech Stack Version**: 1.0.0  
**Last Updated**: January 2026  
**Maintained By**: Kaustubh Mukdam

---

## Next Steps

1. ✅ Review and approve tech stack
2. ⏳ Set up development environment
3. ⏳ Initialize backend project
4. ⏳ Initialize frontend project
5. ⏳ Configure CI/CD pipelines
6. ⏳ Begin Sprint 1 development

For detailed implementation, see:
- [SDLC.md](./SDLC.md) - Development phases
- [PRD.md](./PRD.md) - Product requirements
- [FOLDER_STRUCTURE.md](./FOLDER_STRUCTURE.md) - Project structure