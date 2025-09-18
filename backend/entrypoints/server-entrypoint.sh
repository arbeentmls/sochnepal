#!/bin/bash

set -e

echo "Waiting for AI service to be ready..."
until curl -f http://ai-service:8001/health; do
  echo "AI service is unavailable - sleeping"
  sleep 2
done

echo "AI service is ready!"


until uv run manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

until uv run manage.py collectstatic --noinput
do
    echo "Docker: collecting static"
done

echo "Docker: Populating categories..."
uv run manage.py populate_categories --overwrite

echo "Docker: start django application"
uv run manage.py runserver 0.0.0.0:8000

