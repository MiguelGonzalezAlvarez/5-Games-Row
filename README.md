# 5 Games in a Row - Manchester United Haircut Challenge Tracker

A web application tracking Frank Ilett's (@TheUnitedStrand) viral haircut challenge - he won't cut his hair until Manchester United wins 5 games in a row!

## 🏗 Architecture

```
5-games-row/
├── backend/               # FastAPI Python backend
│   ├── app/
│   │   ├── api/         # API endpoints, WebSockets, Notifications
│   │   ├── core/        # Config, security, JWT, middleware
│   │   ├── db/          # Database setup
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic + caching
│   └── tests/          # Unit & integration tests
│
└── frontend/            # Astro + React + TypeScript
    ├── src/
    │   ├── components/  # React components
    │   ├── pages/      # Astro pages
    │   ├── stores/     # Zustand state
    │   ├── styles/    # CSS + Dark mode
    │   ├── utils/     # API, WebSocket, Supabase, helpers
    │   └── __tests__/ # Tests
    └── public/        # Static assets + PWA
```

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Astro 4.x + React 18 + TypeScript |
| Backend | FastAPI (Python 3.11) |
| Database | SQLite (dev) / PostgreSQL (prod) / Supabase (optional) |
| API Data | football-data.org (free tier) |
| Styling | CSS Modules + Dark/Light Theme |
| State | Zustand |
| Auth | JWT + Supabase Auth (optional) |
| Caching | In-memory cache with TTL |
| Animations | Framer Motion |
| Real-time | WebSockets |
| Push | Web Push Notifications |
| Testing | pytest + Vitest |
| DevOps | Docker, GitHub Actions, nginx |

## ✨ Features

### Core
- **Haircut Counter** - Real-time tracking of days since challenge started (Oct 5, 2024)
- **Streak Tracker** - Shows Manchester United's current winning streak
- **League Table** - Live Premier League standings with MUFC highlighted
- **Match History** - Recent Manchester United results
- **Haircut Simulator** - Visual simulation of hair growth over time
- **Match Predictor** - Predict match scores and track accuracy
- **Historical Stats** - Analysis of United's winning streaks
- **Community Feed** - Share photos and support the challenge

### Technical
- **Smart Caching** - In-memory cache to reduce API calls
- **Rate Limiting** - 60 requests/minute per IP
- **Request Logging** - Complete request/response logging
- **Error Handling** - Centralized error handling middleware
- **JWT Authentication** - Secure user authentication
- **WebSockets** - Real-time updates for matches, standings, challenges
- **Push Notifications** - Web Push API support
- **Dark/Light Theme** - System-aware theme switching
- **PWA** - Installable as a native app with offline support
- **Docker** - Containerized deployment
- **CI/CD** - Automated testing and deployment
- **Tests** - Comprehensive test coverage

## 🚀 Quick Start

### Prerequisites

- Python 3 Node.js 18.11+
-+
- Docker & Docker Compose
- API key from [football-data.org](https://football-data.org)

### Docker Compose (Recommended)

```bash
# Clone the repository
cd 5-games-row

# Set environment variables
cp backend/.env.example backend/.env
# Edit .env and add your FOOTBALL_API_KEY

# Run with Docker
docker-compose up --build
```

Access at:
- Frontend: http://localhost:4321
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## 📡 API Endpoints

### Football
- `GET /api/v1/football/standings` - Premier League standings
- `GET /api/v1/football/matches` - All matches
- `GET /api/v1/football/matches/manchester-united` - MUFC matches
- `GET /api/v1/football/challenge/status` - Challenge status
- `GET /api/v1/football/streak/current` - Current streak
- `GET /api/v1/football/streak/history` - Historical streaks

### Community
- `GET /api/v1/community/posts` - Get posts
- `POST /api/v1/community/posts` - Create post (auth)
- `POST /api/v1/community/posts/{id}/like` - Like (auth)
- `POST /api/v1/community/posts/{id}/comments` - Comment (auth)
- `GET /api/v1/community/predictions/stats` - Prediction stats

### Auth
- `POST /api/v1/community/auth/register` - Register
- `POST /api/v1/community/auth/login` - Login
- `GET /api/v1/community/auth/me` - Get current user

### WebSockets
- `/api/v1/ws/ws/{channel}` - Real-time updates
- Channels: `match_updates`, `challenge_updates`, `standings_updates`

### Notifications
- `POST /api/v1/notifications/subscribe` - Subscribe to push
- `POST /api/v1/notifications/notify` - Broadcast notification

## 🧪 Testing

```bash
# Backend
cd backend
pytest tests/ -v --cov=app

# Frontend
cd frontend
npm test
npm run test:coverage
```

## 📁 Environment Variables

See `backend/.env.example` and `frontend/.env.example` for all configuration options.

## 🐳 Docker Commands

```bash
# Development
docker-compose up -d

# Production
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f

# Rebuild
docker-compose build --no-cache
```

## 📝 License

MIT License

## 🚀 Deployment

### Frontend - GitHub Pages (Solo modo demo)

El frontend está configurado para desplegarse en GitHub Pages usando la rama `gh-pages`:

```bash
cd frontend
npm install
npm run build
npm run deploy
```

**URL**: https://miguelgonzalezalvarez.github.io/5-Games-Row

> **Nota**: El modo demo funciona sin backend. Para conectar el backend, ver más abajo.

### Backend - Railway (Opcional)

Para desplegar el backend en Railway:

1. Crea un proyecto en [Railway](https://railway.app)
2. Conecta tu repositorio GitHub
3. Selecciona la carpeta `backend`
4. Añade las variables de entorno necesarias (ver `backend/.env.example`)
5. Una vez desplegado, copia la URL (ej: `https://tu-proyecto.up.railway.app`)

#### Configurar frontend con backend:

Edita `frontend/.env`:
```bash
PUBLIC_API_URL=https://tu-proyecto.up.railway.app/api/v1
```

Luego redeploya el frontend:
```bash
cd frontend
npm run build
npm run deploy
```

### Procfile (Railway)

El archivo `backend/Procfile` está preparado para Railway:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## ⚠️ Disclaimer

This project is not affiliated with Manchester United FC, football-data.org, or Frank Ilett. It's a fan project created for educational purposes.
