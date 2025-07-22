# SochNepal AI Coding Agent Instructions

SochNepal is a civic engagement platform for reporting and tracking community issues in Nepal. Built as a microservices architecture with Django REST API, Next.js frontend, and containerized deployment.

## 🏗️ Architecture Overview

**Three-tier structure:**

-   `backend/` - Django REST API with JWT auth, Celery workers, PostgreSQL
-   `frontend/` - Next.js 14 with App Router, TypeScript, Tailwind CSS, React Query
-   `ai-service/` - Separate Python service for content moderation (sentiment/toxicity analysis)

**Key integrations:**

-   JWT cookies for stateless auth between frontend/backend
-   Celery + Redis for async tasks (email verification, AI moderation)
-   Cloudinary for image storage
-   Docker Compose for local development

## 🚀 Development Workflows

**Start development environment:**

```bash
# Full stack with Docker
make up  # or docker compose up

# Individual services (requires local setup)
make backend  # cd backend && uv run manage.py runserver
make frontend # cd frontend && npm run dev
```

**Database operations:**

```bash
# In backend container or with uv locally
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

**Fresh environment:**

```bash
make fresh  # Destroys volumes, rebuilds, and starts
```

## 🔐 Authentication Pattern

-   Custom User model with email as USERNAME_FIELD (no username)
-   JWT stored in HTTP-only cookies via `TokenObtainPairViewCookie`
-   User verification required for creating reports (`IsVerifiedUserOrReadOnly`)
-   Email verification handled by Celery task `send_verification_email`

**Frontend auth state:** Zustand store (`store/authStore.ts`) with localStorage persistence

## 📊 Data Models & Relationships

**Core entities:**

-   `User` (custom, email-based) ↔ `Profile` (OneToOne)
-   `Report` (main entity) → `Category`, `User` (creator), location (lat/lng)
-   `Comment` → `Report`, `User`
-   `UpVote` → `Report`, `User` (unique together)
-   `Flag` → `Report`, `User` (for content moderation)

**Status flow:** `pending` → `in_progress` → `resolved`/`rejected`

## 🛠️ Backend Patterns

**App structure:** Features organized as Django apps (`apps/accounts`, `apps/reports`, etc.)
**API versioning:** All endpoints under `/api/v1/`
**Permissions:** Custom classes in `apps/permissions.py` (e.g., `IsVerifiedUserOrReadOnly`)
**Filtering:** django-filter for report queries (status, category, search)
**Pagination:** Custom `ReportPagination` class

**ViewSet example:**

```python
class ReportViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, IsVerifiedUserOrReadOnly]
    # Optimized queryset with select_related and prefetch_related
```

## 🎨 Frontend Patterns

**State management:**

-   React Query for server state (`hooks/use-*.ts` pattern)
-   Zustand for client state (auth, minimal global state)

**API integration:**

```typescript
// Custom axios instance with base URL and credentials
export const customAxios = axios.create({
    baseURL: "http://localhost:8000/api/v1",
    withCredentials: true,
});
```

**Component structure:**

-   `components/ui/` - Shadcn/ui base components
-   `components/[feature]/` - Feature-specific components
-   `app/(dashboard)/` and `app/(general)/` - Route groups

**Custom hooks pattern:** `use-reports.ts`, `use-comments.ts` etc. for data fetching

## 🔧 Key Configuration Files

-   `backend/core/settings.py` - Django settings with django-environ
-   `backend/core/celery.py` - Celery configuration
-   `frontend/lib/customAxios.ts` - API client configuration
-   `docker-compose.yml` - Multi-service development environment
-   `Makefile` - Development shortcuts

## ⚠️ Critical Conventions

**Backend:**

-   Use `uv` for Python dependency management (not pip)
-   All async tasks as Celery `@shared_task`
-   Custom permissions inherit from `BasePermission`
-   Models use `related_name` for reverse relationships

**Frontend:**

-   TypeScript strict mode enabled
-   All API calls through custom hooks with React Query
-   Form validation with React Hook Form + Zod
-   Responsive design with Tailwind CSS utility classes

**Docker:**

-   Separate entrypoints for server vs worker containers
-   Volume mounts for development hot-reload
-   Named volumes for persistent data

## 🌍 Nepal-Specific Context

-   Phone numbers validated for Nepal region (`region="NP"`)
-   Bilingual support (English/Nepali) in category names
-   Geographic coordinates required for all reports (Nepal-focused mapping)
