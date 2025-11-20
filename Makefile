.PHONY: backend frontend

backend:
	cd backend && uv run manage.py runserver
frontend:
	cd frontend && npm run dev
ai:
	cd ai-service && uv run fastapi run --port=8001
worker:
	cd backend && uv run celery -A core worker -l INFO

up:
	docker compose up

down:
	docker compose down

build:
	docker compose build

fresh:
	docker compose down --volumes && docker compose build && docker compose up