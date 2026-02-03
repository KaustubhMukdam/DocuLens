# DocuLens Backend

FastAPI-based backend for the DocuLens learning platform.

---

## 🏗️ Architecture

```
backend/
├── app/
│   ├── api/                 # API endpoints
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── languages.py
│   │       ├── docs.py
│   │       ├── videos.py
│   │       ├── practice.py
│   │       ├── progress.py
│   │       ├── bookmarks.py
│   │       └── ...
│   ├── core/                # Core configuration
│   │   ├── config.py
│   │   ├── security.py
│   │   └── logging.py
│   ├── crud/                # CRUD operations
│   ├── db/                  # Database setup
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   └── services/            # Business logic
├── alembic/                 # Database migrations
├── logs/                    # Application logs
├── requirements.txt         # Dependencies
└── .env.example             # Environment template
```

---

## 🚀 Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create `.env` file:

```bash
cp .env.example .env
```

Required variables:

```env
# App
ENVIRONMENT=development
DEBUG=True

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/doculens

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# AI Services
GROQ_API_KEY=your-groq-key
ANTHROPIC_API_KEY=your-anthropic-key

# Optional
REDIS_URL=redis://localhost:6379/0
```

### 4. Initialize Database

```bash
# Run migrations
alembic upgrade head

# Seed initial data (optional)
python scripts/seed_data.py
```

### 5. Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at:

- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📚 API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/refresh` - Refresh token

### Languages

- `GET /api/v1/languages` - List all languages
- `GET /api/v1/languages/{slug}` - Get language by slug
- `POST /api/v1/languages` - Create language (admin)

### Documentation Sections

- `GET /api/v1/docs/{language}/sections` - Get sections by language
- `GET /api/v1/docs/sections/{id}` - Get section details
- `POST /api/v1/docs/sections` - Create section (admin)

### Videos

- `GET /api/v1/videos/sections/{id}` - Get videos for section
- `POST /api/v1/videos/sections/{id}/scrape` - Scrape YouTube videos

### Practice Problems

- `GET /api/v1/practice/sections/{id}` - Get problems for section
- `POST /api/v1/practice/sections/{id}/scrape` - Scrape LeetCode problems

### Progress

- `GET /api/v1/progress/me` - Get user progress
- `GET /api/v1/progress/stats` - Get progress statistics
- `POST /api/v1/progress/sections/{id}/complete` - Mark section complete

### Bookmarks

- `GET /api/v1/bookmarks` - Get user bookmarks
- `POST /api/v1/bookmarks` - Create bookmark
- `DELETE /api/v1/bookmarks/{id}` - Delete bookmark

> **Full API documentation available at `/docs` when server is running.**

---

## 🗄️ Database Models

- **User**: User accounts and authentication
- **Language**: Programming languages (Python, JavaScript, etc.)
- **DocSection**: Documentation sections
- **VideoResource**: YouTube tutorial videos
- **PracticeProblem**: LeetCode/HackerRank problems
- **UserProgress**: Learning progress tracking
- **Bookmark**: Saved sections
- **Discussion**: Community discussions (future)

---

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py
```

---

## 🔧 Development Tools

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Code Formatting

```bash
# Format code with Black
black app/

# Check code style
flake8 app/
```

### Run with Docker (Optional)

```bash
docker-compose up -d
```

---

## 📝 Environment Setup

### For Production

```env
ENVIRONMENT=production
DEBUG=False
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
CORS_ORIGINS=https://yourdomain.com
```

### For Development

```env
ENVIRONMENT=development
DEBUG=True
DATABASE_URL=postgresql+asyncpg://localhost:5432/doculens_dev
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## 🚀 Deployment

> **Note**: Production deployment is planned for Phase 2.

**Recommended platforms:**

- **Render** (Free tier available)
- **Railway** (Easy PostgreSQL setup)
- **Fly.io** (Global deployment)
- **AWS/GCP/Azure** (Enterprise)

---

## 🔐 Security

- ✅ JWT-based authentication
- ✅ Password hashing with bcrypt
- ✅ CORS protection
- ⏳ Rate limiting (planned)
- ✅ Input validation with Pydantic
- ✅ SQL injection prevention (SQLAlchemy ORM)

---

## 📊 Performance

- ⚡ Async/await throughout
- 🔌 Database connection pooling
- 💾 Redis caching (optional)
- 🔗 Lazy loading of relationships
- 📄 Efficient pagination

---

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
psql -U postgres

# Test connection string
python -c "from app.db.session import engine; print(engine)"
```

### Migration Errors

```bash
# Reset database (CAUTION: destroys data)
alembic downgrade base
alembic upgrade head
```

---

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)
- [Pydantic Validation](https://docs.pydantic.dev/)

---

## 🤝 Contributing

See main [README.md](../README.md) for contribution guidelines.

---

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details.