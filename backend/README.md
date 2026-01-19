# 🎓 DocuLens Backend - AI-Powered Documentation Learning Platform

> Transform official documentation into structured, gamified learning experiences with AI-powered insights.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Features

### 📚 Content Management
- **Automated Documentation Scraping** - Fetch and parse official programming language docs
- **AI-Powered Summaries** - Groq Llama 3.3 & Claude Sonnet 4 integration
- **Code Example Extraction** - Automatic code snippet extraction and highlighting
- **Video Curation** - YouTube API integration for tutorial recommendations

### 🎮 Gamification
- **Learning Paths** - Quick (11 hours) and Deep (23 hours) tracks
- **Progress Tracking** - Section completion, streaks, and milestones
- **Difficulty Levels** - Easy, Medium, Hard content classification
- **Bookmarks & Notes** - Personal learning workspace

### 🔐 Security & Auth
- **JWT Authentication** - Secure token-based auth with refresh tokens
- **Role-Based Access** - Admin and user permissions
- **Password Reset** - Email-based password recovery
- **Rate Limiting** - API protection and abuse prevention

### 👨‍💼 Admin Panel
- **Content Scraping** - One-click documentation import
- **Video Management** - Bulk YouTube video addition
- **User Management** - Promote users, view statistics
- **Analytics Dashboard** - Platform usage metrics

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 16+
- Redis (optional, for caching)

### Installation

```bash
# Clone repository
git clone https://github.com/KaustubhMukdam/doculens-backend.git
cd doculens-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### Environment Variables

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/doculens

# Security
SECRET_KEY=your-super-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# AI Services
GROQ_API_KEY=your-groq-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key

# YouTube
YOUTUBE_API_KEY=your-youtube-api-key

# SMTP (Email)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Database Setup

```bash
# Initialize database
psql -U postgres
CREATE DATABASE doculens;
\q

# Run migrations (automatically on startup)
uvicorn app.main:app --reload
```

### Run Server

```bash
# Development
uvicorn app.main:app --reload --port 8000

# Production
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

**Access:**
- API Documentation: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## 📊 Database Schema

### Core Models

| Model | Description |
|-------|-------------|
| **User** | Authentication, profiles, gamification stats |
| **Language** | Programming languages (Python, JavaScript, etc.) |
| **DocSection** | Documentation sections with AI summaries |
| **VideoResource** | Curated YouTube tutorials |
| **PracticeProblem** | Coding challenges (LeetCode, etc.) |
| **UserProgress** | Section completion tracking |
| **LearningPath** | Personalized learning tracks |
| **Discussion** | Community Q&A |
| **Bookmark** | User-saved sections |

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI 0.109+ |
| Database | PostgreSQL 16 + SQLAlchemy 2.0 |
| Authentication | JWT + Passlib (bcrypt) |
| AI Models | Groq Llama 3.3, Claude Sonnet 4 |
| Web Scraping | BeautifulSoup4, httpx |
| Validation | Pydantic v2 |
| Testing | pytest, pytest-asyncio |
| API Docs | OpenAPI 3.1 (Swagger UI) |

## 📡 API Endpoints

### Authentication
```
POST   /api/v1/auth/register        - Register new user
POST   /api/v1/auth/login           - Login
POST   /api/v1/auth/refresh         - Refresh access token
POST   /api/v1/auth/password-reset  - Request password reset
```

### Languages & Content
```
GET    /api/v1/languages            - List all languages
GET    /api/v1/languages/{slug}     - Get language details
GET    /api/v1/sections             - Get documentation sections
GET    /api/v1/sections/{id}        - Get section with videos
```

### Learning Paths
```
POST   /api/v1/learning-paths       - Create learning path
GET    /api/v1/learning-paths/me    - Get my paths
GET    /api/v1/languages/{slug}/learning-path - Get recommended path
```

### Progress Tracking
```
POST   /api/v1/progress/mark-complete - Mark section complete
GET    /api/v1/progress/me            - Get my progress
GET    /api/v1/progress/stats         - Get detailed stats
```

### Admin (Auth Required)
```
GET    /api/v1/admin/stats              - Dashboard stats
POST   /api/v1/admin/scrape/language    - Scrape documentation
POST   /api/v1/admin/scrape/videos/{id} - Add videos
POST   /api/v1/admin/users/promote      - Promote to admin
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

## 📈 Current Data

- **Languages:** 1 (Python)
- **Sections:** 30 (Official Python Tutorial)
- **Videos:** 156 (Curated YouTube)
- **Quick Path:** 12 sections (~11 hours)
- **Deep Path:** 30 sections (~23 hours)

## 🔄 Scraping New Content

### Scrape Python Documentation

```bash
curl -X POST "http://localhost:8000/api/v1/admin/scrape/language" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "language_name": "Python",
    "official_doc_url": "https://docs.python.org/3/",
    "add_videos": true
  }'
```

## 🚀 Deployment

### Docker (Coming Soon)
```bash
docker-compose up -d
```

### Render / Railway
1. Push to GitHub
2. Connect repository
3. Set environment variables
4. Deploy!

## 📝 Project Structure

```
backend/
├── app/
│   ├── api/v1/          # API endpoints
│   ├── core/            # Config, security, logging
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── crud/            # Database operations
│   ├── services/        # Business logic
│   ├── scrapers/        # Web scraping modules
│   └── main.py          # FastAPI app
├── tests/               # Test suite
├── alembic/             # Database migrations
├── logs/                # Application logs
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
└── README.md
```

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Groq](https://groq.com/) - Fast AI inference
- [Anthropic](https://anthropic.com/) - Claude AI
- [Python Documentation](https://docs.python.org/) - Content source

## 📧 Contact

**Kaustubh Mukdam**
- GitHub: [@kaustubhmukdam](https://github.com/kaustubhmukdam)
- Email: kaustubhmukdam7@gmail.com

---

Built with ❤️ for developers who learn from documentation