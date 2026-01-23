# DocuLens Frontend

## Setup

### 1. Install dependencies
```bash
npm install
```

### 2. Create `.env` file
```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_NAME=DocuLens
```

### 3. Run development server
```bash
npm run dev
```

### 4. Build for production
```bash
npm run build
```

### 5. Preview production build
```bash
npm run preview
```

## Backend Connection

Make sure your FastAPI backend is running on `http://localhost:8000`

## Features

- ✅ Authentication (Login/Register/Logout)
- ✅ Dashboard with progress stats
- ✅ Browse programming languages
- ✅ View documentation sections
- ✅ Track learning progress
- ✅ AI-powered summaries
- ✅ Personalized learning paths

## Getting Started (Full Stack)

### Terminal 1 - Backend
```bash
cd DocuLens/backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m app.main
```

### Terminal 2 - Frontend
```bash
cd DocuLens/frontend
npm run dev
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🚀 Production Deployment

### Frontend (Vercel/Netlify)

1. Build the project:
```bash
npm run build
```

2. Deploy the `dist` folder to your hosting provider

3. Set environment variables:
```bash
VITE_API_BASE_URL=https://api.doculens.dev/api/v1
```

### Backend (Railway/Render)

- Already configured in your `.env`
- **Important**: Update `CORS_ORIGINS` in backend settings to include your production frontend domain

---

**Note**: Ensure both frontend and backend are running simultaneously for full functionality during development.