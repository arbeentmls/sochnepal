# SochNepal 🏛️A collaboration project by @bluescorpio01234 and @sulavmhrzh.

A civic engagement platform that empowers Nepali citizens to report, track, and resolve community issues. Built to strengthen democracy through digital participation and government accountability.

## 🚀 Features

-   **Report Civic Issues** - Submit reports with photos, location, and detailed descriptions
-   **Real-time Tracking** - Track issue status and government responses
-   **Community Engagement** - Vote, comment, and discuss civic matters
-   **Email Verification** - Secure user authentication and verification

## 🛠️ Tech Stack

### Backend

-   **Django** - Python web framework
-   **Django REST Framework** - API development
-   **PostgreSQL** - Primary database
-   **Redis** - Caching and broker
-   **Celery** - Background task processing
-   **JWT** - Authentication

### Frontend

-   **Next.js 14** - React framework with App Router
-   **TypeScript** - Type-safe development
-   **Tailwind CSS** - Utility-first styling
-   **React Query** - Data fetching and caching
-   **Zustand** - State management
-   **Shadcn/ui** - UI component library

### DevOps

-   **Docker** - Containerization
-   **Docker Compose** - Multi-container orchestration

## 📁 Project Structure

```
sochnepal/
├── backend/                 # Django REST API
│   ├── apps/
│   │   ├── accounts/       # User management
│   │   ├── reports/        # Civic issue reports
│   │   ├── flags/          # Report flagging system
│   │   └── permissions/    # Custom permissions
│   ├── core/               # Project settings
│   ├── requirements.txt    # Python dependencies
│   └── .env.example       # Environment variables template
├── frontend/               # Next.js application
│   ├── app/               # App router pages
│   ├── components/        # Reusable components
│   ├── hooks/            # Custom React hooks
│   ├── lib/              # Utilities and configurations
│   └── store/            # State management
├── docker-compose.yml     # Docker services configuration
└── README.md
```

## 🚀 Quick Start

### Prerequisites

-   **Docker** and **Docker Compose**
-   **Git**

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/sochnepal.git
cd sochnepal
```

### 2. Environment Setup

```bash
# Copy environment file
cp backend/.env.example backend/.env

# Edit the .env file with your configurations
nano backend/.env
```

### 3. Environment Variables

Update `backend/.env` with your settings:

```env
# Database
POSTGRES_DB=sochnepal
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Django
SECRET_KEY=your_super_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email (for verification)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Redis
REDIS_URL=redis://redis:6379/0

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

### 4. Run with Docker

```bash
# Build and start all services
docker compose up --build

# Or run in background
docker compose up -d --build
```

### 5. Initialize Database

```bash
# Create superuser (optional)
docker compose exec backend python manage.py createsuperuser

# Populate default categories
docker compose exec backend python manage.py populate_categories
```

### 6. Access the Application

-   **Frontend**: http://localhost:3000
-   **Backend API**: http://localhost:8000
-   **Admin Panel**: http://localhost:8000/admin

## 🐳 Docker Services

The application runs the following services:

-   **db** - PostgreSQL database (port 5433)
-   **redis** - Redis cache and message broker
-   **backend** - Django API server (port 8000)
-   **frontend** - Next.js application (port 3000)
-   **worker** - Celery background tasks

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🆘 Support

-   **Issues**: [GitHub Issues](https://github.com/sulavmhrzn/sochnepal/issues)
-   **Discussions**: [GitHub Discussions](https://github.com/sulavmhrzn/sochnepal/discussions)

**SochNepal** - Empowering citizens, strengthening democracy 🏛️✊
