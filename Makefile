.PHONY: help install dev start stop clean test load-data

help:
	@echo "OpenAudit Visualizer - Available Commands:"
	@echo ""
	@echo "  make install      - Install all dependencies (backend + frontend)"
	@echo "  make dev          - Start development servers (all services)"
	@echo "  make start        - Start production build with Docker Compose"
	@echo "  make stop         - Stop all Docker services"
	@echo "  make load-data    - Load CSV data into database"
	@echo "  make clean        - Clean build artifacts and caches"
	@echo "  make test         - Run tests for backend and frontend"
	@echo "  make logs         - View Docker logs"
	@echo "  make shell-db     - Open PostgreSQL shell"
	@echo "  make shell-backend - Open backend container shell"
	@echo ""

install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Installation complete!"

dev:
	@echo "Starting all services with Docker Compose..."
	docker-compose up

start:
	@echo "Starting services in detached mode..."
	docker-compose up -d
	@echo "Services started! Frontend: http://localhost:5173, Backend: http://localhost:8000"

stop:
	@echo "Stopping all services..."
	docker-compose down

load-data:
	@echo "Loading data into database..."
	docker-compose exec backend python scripts/load_data.py

clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	cd frontend && rm -rf dist node_modules/.vite 2>/dev/null || true
	@echo "Clean complete!"

test:
	@echo "Running backend tests..."
	cd backend && pytest
	@echo "Running frontend tests..."
	cd frontend && npm test

logs:
	docker-compose logs -f

shell-db:
	docker-compose exec postgres psql -U openaudit_user -d openaudit

shell-backend:
	docker-compose exec backend /bin/bash

build:
	@echo "Building Docker images..."
	docker-compose build
