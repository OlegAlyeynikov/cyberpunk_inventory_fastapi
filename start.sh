#!/bin/bash

echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

alembic upgrade head

uvicorn inventory_api.main:app --host 0.0.0.0 --reload
