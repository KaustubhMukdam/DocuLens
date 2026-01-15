# 🚀 DocuLens - AI-Powered Documentation Learning Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Flutter](https://img.shields.io/badge/Flutter-3.22+-02569B.svg?style=flat&logo=Flutter&logoColor=white)](https://flutter.dev)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

> *"Transform lengthy documentation into personalized learning journeys"*

---

## 📖 Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**DocuLens** is an innovative learning platform that transforms overwhelming official documentation into personalized, AI-curated learning paths. We solve the problem of information overload by offering two learning modes:

- **Quick Path** (20-30% content): Essential concepts for rapid learning
- **Deep Path** (100% content): Comprehensive coverage with practice integration

### The Problem We Solve

- 📚 **Information Overload**: Official docs are comprehensive but time-consuming
- 🤖 **AI Unreliability**: ChatGPT/Claude can hallucinate or provide outdated info
- 🔗 **Fragmented Resources**: Documentation, videos, and practice problems are scattered
- 📊 **No Progress Tracking**: Hard to maintain learning momentum
- 📱 **Poor Mobile Experience**: Most documentation isn't mobile-optimized

### Our Solution

DocuLens provides:
- ✅ **Source-Verified Content**: Every summary links back to official documentation
- ✅ **Dual Learning Paths**: Choose between Quick (8-15 hrs) and Deep (40-60 hrs)
- ✅ **Integrated Practice**: LeetCode, HackerRank problems mapped to topics
- ✅ **Cross-Platform**: Seamless experience on Web, iOS, and Android
- ✅ **Progress Tracking**: Complete analytics and achievement system

---

## 🌟 Key Features

### For Learners

- **🎯 Personalized Learning Paths**
  - Skill-based recommendations (Beginner/Intermediate/Advanced)
  - Adaptive difficulty progression
  - Estimated time for each section

- **📝 AI-Curated Summaries**
  - Powered by Claude Sonnet 4
  - 95%+ accuracy with source attribution
  - View full documentation anytime

- **💪 Practice Integration**
  - Curated problems from LeetCode, HackerRank
  - Difficulty mapping (Easy/Medium/Hard)
  - Track solved problems

- **📊 Progress Analytics**
  - Time spent tracking
  - Completion statistics
  - Learning streak system
  - Achievement badges

- **🔍 Smart Search**
  - Semantic search across all content
  - Filter by language, difficulty, topic
  - Recent searches history

### For the Platform

- **🤖 Automated Content Pipeline**
  - Scheduled scraping of official docs
  - AI-powered summarization
  - Version control for updates

- **🔐 Secure & Scalable**
  - JWT authentication
  - Rate limiting
  - Horizontal scaling ready

- **📱 Cross-Platform**
  - Flutter for Web, iOS, Android
  - Consistent experience across devices
  - Offline mode support (coming soon)

---

## 💻 Tech Stack

### Backend
- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL 15+ with Redis caching
- **AI**: Anthropic Claude API (Sonnet 4)
- **Task Queue**: Celery + RabbitMQ
- **Scraping**: BeautifulSoup4, Scrapy, Playwright

### Frontend
- **Framework**: Flutter 3.22+ (Web, iOS, Android)
- **State Management**: Riverpod 2.4+
- **Networking**: Dio 5.4+ with Retrofit
- **Local Storage**: Hive 2.2+

### DevOps
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Hosting**: AWS / DigitalOcean
- **Monitoring**: Sentry, Prometheus, Grafana

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+ (for Flutter web)
- PostgreSQL 15+
- Redis 7+
- Flutter SDK 3.22+
- Docker & Docker Compose (optional)

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/KaustubhMukdam/DocuLens.git
cd DocuLens

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Start all services
docker-compose up -d

# Backend will be available at http://localhost:8000
# Frontend will be available at http://localhost:3000
```

### Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configurations

# Initialize database
alembic upgrade head
python scripts/init_db.py

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Get Flutter dependencies
flutter pub get

# Run code generation (if needed)
flutter pub run build_runner build --delete-conflicting-outputs

# Run the app
flutter run -d chrome  # For web
flutter run -d ios     # For iOS
flutter run -d android # For Android
```

### Initial Data Seeding

```bash
cd backend

# Seed initial languages
python scripts/seed_data.py

# Start scraping (optional - runs in background)
python scripts/run_scraper.py --language python
```

---

## 📂 Project Structure

```
DocuLens/
├── backend/           # FastAPI backend
├── frontend/          # Flutter frontend
├── docs/              # Project documentation
├── scripts/           # Utility scripts
├── .github/           # GitHub workflows
└── docker-compose.yml # Multi-container setup
```

For detailed structure, see [ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 📚 Documentation

- **[Architecture](docs/ARCHITECTURE.md)**: System design and architecture
- **[API Documentation](docs/API.md)**: Complete API reference
- **[PRD](docs/PRD.md)**: Product Requirements Document
- **[SDLC](docs/SDLC.md)**: Complete Software Development Life Cycle
- **[Deployment](docs/DEPLOYMENT.md)**: Deployment guides
- **[Contributing](docs/CONTRIBUTING.md)**: How to contribute

---

## 🎨 Screenshots

> *Coming Soon - Add screenshots once UI is implemented*

---

## 🗺️ Roadmap

### Phase 1: MVP (Months 1-3) ✅ In Progress
- [x] Authentication system
- [x] Documentation scraping pipeline
- [x] AI summarization
- [x] Quick & Deep learning paths
- [ ] Flutter app (Web, iOS, Android)
- [ ] Progress tracking

### Phase 2: Enhancement (Months 4-6)
- [ ] Video integration (YouTube API)
- [ ] Code playground
- [ ] Community discussions
- [ ] AI chatbot for Q&A
- [ ] Offline mode
- [ ] Custom learning paths

### Phase 3: Growth (Months 7-12)
- [ ] Achievements & gamification
- [ ] Mentor matching system
- [ ] Team/Enterprise features
- [ ] API for educational institutions
- [ ] Mobile apps on stores
- [ ] Premium subscription

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- **Backend**: Follow PEP 8, use Black for formatting
- **Frontend**: Follow Dart style guide, use `flutter analyze`

---

## 📊 Project Stats

- **Languages**: Python, Dart
- **Target Users**: 10M+ developers worldwide
- **Initial Focus**: Python, Flutter, JavaScript, React
- **Goal**: Reduce learning time by 60%

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

**Project Lead & Developer**: Kaustubh Mukdam
- GitHub: [@KaustubhMukdam](https://github.com/KaustubhMukdam)
- Email: kaustubhmukdam7@gmail.com

---

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) for Claude AI API
- [FastAPI](https://fastapi.tiangolo.com/) for the amazing framework
- [Flutter](https://flutter.dev/) for cross-platform capabilities
- All open-source contributors

---

## 📞 Support

- **Documentation**: [docs.doculens.dev](https://docs.doculens.dev)
- **Issues**: [GitHub Issues](https://github.com/KaustubhMukdam/DocuLens/issues)
- **Discussions**: [GitHub Discussions](https://github.com/KaustubhMukdam/DocuLens/discussions)
- **Email**: kaustubhmukdam7@gmail.com

---

**Made with ❤️ for developers, by developers**

⭐ Star us on GitHub if you find this project useful!