# DocuLens Frontend

React-based frontend for the DocuLens learning platform.

---

## 🏗️ Architecture

```
frontend/
├── public/                  # Static assets
├── src/
│   ├── api/                # API client
│   ├── components/         # React components
│   │   ├── auth/          # Authentication components
│   │   ├── common/        # Reusable components
│   │   └── layout/        # Layout components
│   ├── context/           # React contexts
│   ├── pages/             # Page components
│   ├── store/             # Zustand stores
│   ├── utils/             # Utility functions
│   ├── App.jsx            # Main app component
│   └── main.jsx           # Entry point
├── .env.example           # Environment template
├── package.json           # Dependencies
├── tailwind.config.js     # Tailwind configuration
└── vite.config.js         # Vite configuration
```

---

## 🚀 Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Variables

Create `.env` file:

```bash
cp .env.example .env
```

Required variables:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### 3. Run Development Server

```bash
npm run dev
```

**App will be available at:** http://localhost:5173

---

## 📦 Available Scripts

```bash
# Development
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build

# Code Quality
npm run lint         # Run ESLint
npm run format       # Format with Prettier

# Testing (planned)
npm run test         # Run tests
npm run test:ui      # Run tests with UI
npm run test:coverage # Run tests with coverage
```

---

## 🎨 Tech Stack

- **React 18.2+**: UI library
- **Vite 7.3**: Build tool & dev server
- **React Router v6**: Routing
- **TailwindCSS 3.4**: Styling
- **React Query**: Server state management
- **Zustand**: Client state management
- **Axios**: HTTP client
- **Lucide React**: Icons
- **React Hot Toast**: Notifications

---

## 📂 Key Components

### Pages

- `Home.jsx` - Landing page
- `Login.jsx` - User login
- `Register.jsx` - User registration
- `Dashboard.jsx` - User dashboard with stats
- `Languages.jsx` - Programming languages list
- `LanguageDetail.jsx` - Language sections view
- `SectionDetail.jsx` - Documentation section details
- `Profile.jsx` - User profile & settings
- `Bookmarks.jsx` - Saved sections
- `NotFound.jsx` - 404 error page

### Components

- `Navbar.jsx` - Navigation bar with auth state
- `SearchBar.jsx` - Global search component
- `Loading.jsx` - Loading spinner
- `Toast.jsx` - Toast notifications
- `ErrorBoundary.jsx` - Error handling
- `ProtectedRoute.jsx` - Route protection

---

## 🗄️ State Management

### Zustand Stores:

```javascript
// authStore.js - Authentication state
{
  user: null,
  token: null,
  isAuthenticated: false,
  login: (token, user) => {},
  logout: () => {},
  initAuth: async () => {}
}
```

### React Query:

- Used for all server data fetching
- Automatic caching & revalidation
- Loading & error states

---

## 🛣️ Routing

```javascript
/ - Home
/login - Login
/register - Register
/dashboard - Dashboard (protected)
/languages - Languages list (protected)
/languages/:slug - Language sections (protected)
/sections/:id - Section detail (protected)
/profile - User profile (protected)
/bookmarks - Bookmarks (protected)
```

---

## 🎨 Styling

### Tailwind Configuration

```javascript
// tailwind.config.js
{
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {...},
        secondary: {...}
      }
    }
  }
}
```

### Dark Mode

Dark mode is implemented using:

- Context API (`ThemeContext`)
- Tailwind's `dark:` variant
- LocalStorage persistence

Toggle dark mode:

```javascript
const { theme, toggleTheme } = useTheme();
```

---

## 🔐 Authentication

### Authentication Flow:

1. User logs in → receives JWT token
2. Token stored in localStorage
3. Token added to all API requests via Axios interceptor
4. Protected routes check auth state
5. Auto-logout on token expiration

### API Client with Auth:

```javascript
// API client with auth
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

---

## 🚀 Building for Production

```bash
# Build
npm run build

# Preview build locally
npm run preview
```

Build output will be in `dist/` directory.

---

## 📱 Responsive Design

### Breakpoints:

- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

All components are mobile-first and fully responsive.

---

## 🎯 Performance Optimizations

- ⚡ Code splitting with `React.lazy`
- 🖼️ Image optimization
- 💾 React Query caching
- ⌨️ Debounced search
- 📜 Virtual scrolling (planned)
- 🔧 Service Worker (planned)

---

## 🧪 Testing (Planned)

```bash
# Unit tests
npm run test

# E2E tests
npm run test:e2e

# Component tests
npm run test:component
```

---

## 🐛 Troubleshooting

### API Connection Issues

```javascript
// Check environment variable
console.log(import.meta.env.VITE_API_BASE_URL);

// Test API connection
fetch(`${import.meta.env.VITE_API_BASE_URL}/languages`)
  .then(r => r.json())
  .then(console.log);
```

### Build Errors

```bash
# Clear cache
rm -rf node_modules dist
npm install
npm run build
```

---

## 🚀 Deployment

> **Note**: Production deployment is planned for Phase 2.

**Recommended platforms:**

- **Vercel** (Recommended - zero config)
- **Netlify** (Easy CI/CD)
- **AWS Amplify** (AWS integration)
- **GitHub Pages** (Static hosting)

---

## 📚 Resources

- [React Documentation](https://react.dev/)
- [Vite Guide](https://vitejs.dev/)
- [TailwindCSS Docs](https://tailwindcss.com/)
- [React Query Docs](https://tanstack.com/query/latest)
- [React Router Docs](https://reactrouter.com/)

---

## 🤝 Contributing

See main [README.md](../README.md) for contribution guidelines.

---

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details.