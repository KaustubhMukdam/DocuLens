# 🚀 DocuLens - AI-Powered Documentation Learning Platform

*"Transform lengthy documentation into personalized learning journeys"*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18.2+-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg)](https://fastapi.tiangolo.com/)

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [Screenshots](#-screenshots)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**DocuLens** is an innovative learning platform that transforms overwhelming official documentation into personalized, AI-curated learning paths. We solve the problem of information overload by offering two learning modes:

- **Quick Path** (20-30% content): Essential concepts for rapid learning
- **Deep Path** (100% content): Comprehensive coverage with practice integration

---

## 💡 Problem Statement

### The Challenges Developers Face:

- 📚 **Information Overload**: Official docs are comprehensive but time-consuming (1000+ pages)
- 🤖 **AI Unreliability**: ChatGPT/Claude can hallucinate or provide outdated information
- 🔗 **Fragmented Resources**: Documentation, videos, and practice problems are scattered
- 📊 **No Progress Tracking**: Hard to maintain learning momentum and measure growth
- 🎯 **One-Size-Fits-All**: No personalization based on skill level or time constraints

### Our Solution:

DocuLens provides a **unified learning experience** that combines:

- ✅ **Source-Verified Content**: Every summary links back to official documentation
- ✅ **Dual Learning Paths**: Choose between Quick (8-15 hrs) and Deep (40-60 hrs)
- ✅ **Integrated Practice**: LeetCode, HackerRank problems mapped to topics
- ✅ **Video Integration**: Curated YouTube tutorials for visual learners
- ✅ **Progress Analytics**: Complete tracking with streaks and achievements

---

## 🌟 Key Features

### For Learners

#### **📚 Dual Learning Paths**
- **Quick Path**: 20-30% of content - essential concepts only
- **Deep Path**: 100% comprehensive coverage
- Skill-based recommendations (Beginner/Intermediate/Advanced)
- Estimated time for each section

#### **🤖 AI-Curated Summaries**
- Powered by **Claude Sonnet 4** and **Groq**
- 95%+ accuracy with source attribution
- 2-minute summaries of 50-page documentation
- View full documentation anytime

#### **💪 Practice Integration**
- Curated problems from LeetCode, HackerRank
- Difficulty mapping (Easy/Medium/Hard)
- Topic-aligned practice
- Track solved problems

#### **📺 Video Resources**
- Auto-scraped YouTube tutorials
- Relevance-ranked videos
- Multiple learning styles supported

#### **📊 Progress Analytics**
- Time spent tracking
- Completion statistics
- Learning streak system
- Achievement badges
- Personal dashboard

#### **🔍 Smart Search**
- Semantic search across all content
- Filter by language, difficulty, topic
- Recent searches history

#### **🌙 Modern UX**
- Full dark mode support
- Responsive design (mobile-first)
- Clean, intuitive interface
- Accessibility features

---

## 💻 Tech Stack

### Backend
- **Framework**: FastAPI 0.115.6
- **Database**: PostgreSQL 15+ (NeonDB)
- **Caching**: Redis 7+
- **AI Services**: 
  - Anthropic Claude API (Sonnet 4)
  - Groq (llama-3.3-70b)
- **Task Queue**: Celery + RabbitMQ
- **Scraping**: BeautifulSoup4, Scrapy, Playwright
- **ORM**: SQLAlchemy 2.0 (async)
- **Authentication**: JWT with passlib

### Frontend
- **Framework**: React 18.2+ with Vite 7.3
- **State Management**: 
  - React Query (server state)
  - Zustand (client state)
  - Context API (theme)
- **Styling**: TailwindCSS 3.4
- **Routing**: React Router v6
- **UI Components**: Custom + Lucide Icons
- **HTTP Client**: Axios

### DevOps & Tools
- **Version Control**: Git + GitHub
- **Package Management**: pip (backend), npm (frontend)
- **Code Quality**: Black, ESLint, Prettier
- **Environment**: Python 3.11+, Node.js 20+

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 15+
- Redis 7+ (optional, for caching)

### Quick Start

#### 1. Clone the Repository

```bash
git clone https://github.com/KaustubhMukdam/DocuLens.git
cd DocuLens
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configurations

# Initialize database
alembic upgrade head

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be available at:** http://localhost:8000  
**API Documentation:** http://localhost:8000/docs

#### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env (usually just needs VITE_API_BASE_URL)

# Run development server
npm run dev
```

**Frontend will be available at:** http://localhost:5173

---

## 📂 Project Structure

```
DocuLens/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   │   └── v1/         # API version 1
│   │   ├── core/           # Core functionality
│   │   ├── crud/           # Database operations
│   │   ├── db/             # Database config
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── alembic/            # Database migrations
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment template
│
├── frontend/                # React frontend
│   ├── public/             # Static assets
│   ├── src/
│   │   ├── api/            # API client
│   │   ├── components/     # React components
│   │   ├── context/        # React contexts
│   │   ├── pages/          # Page components
│   │   ├── store/          # Zustand stores
│   │   └── utils/          # Utility functions
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
│
├── docs/                    # Documentation
├── .gitignore
└── README.md               # This file
```

---


## 🗺️ Roadmap

### ✅ Phase 1: MVP (Completed)

- ✅ Authentication system (JWT)
- ✅ Documentation scraping pipeline
- ✅ AI summarization (Claude + Groq)
- ✅ Quick & Deep learning paths
- ✅ React frontend with modern UI
- ✅ Progress tracking & analytics
- ✅ Video resource integration
- ✅ Practice problem scraping
- ✅ Bookmark system
- ✅ Search functionality
- ✅ Dark mode support

### 🚀 Phase 2: Production & Enhancement (In Progress)

- ⏳ Production deployment (Vercel + Render)
- ⏳ Additional languages (JavaScript, React, Flutter, Go)
- ⏳ Advanced analytics dashboard
- ⏳ Email notifications
- ⏳ Export progress reports

### 🔮 Phase 3: Growth (Future Scope)

- 🔜 Community discussions forum
- 🔜 Mentor matching system
- 🔜 Team/Enterprise features
- 🔜 Mobile apps (iOS & Android)
- 🔜 API for educational institutions
- 🔜 Premium subscription tier
- 🔜 Gamification & achievements
- 🔜 Code playground integration
- 🔜 Offline mode support
- 🔜 Custom learning path creation

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- **Backend**: Follow PEP 8, use Black for formatting
- **Frontend**: Follow Airbnb React Style Guide, use ESLint + Prettier

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Author

**Kaustubh Mukdam**

- GitHub: [@KaustubhMukdam](https://github.com/KaustubhMukdam)
- LinkedIn: [Kaustubh Mukdam](https://www.linkedin.com/in/kaustubh-mukdam/)
- Email: kaustubhmukdam7@gmail.com

---

## 🙏 Acknowledgments

- FastAPI for the amazing framework
- Anthropic for Claude AI API
- React for the frontend library
- All open-source contributors

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/KaustubhMukdam/DocuLens/issues)
- **Discussions**: [GitHub Discussions](https://github.com/KaustubhMukdam/DocuLens/discussions)
- **Email**: kaustubhmukdam7@gmail.com

---

<div align="center">

**Made with ❤️ for developers, by a developer**

⭐ Star this repo if you find it useful!

</div>