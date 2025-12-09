.PHONY: help install run-backend run-frontend dev stop test clean

# Default Python and npm paths
PYTHON = codingtestsvenv/bin/python
PIP = codingtestsvenv/bin/pip
NPM = npm

help:
	@echo "Django + React Coding Tests Platform - Development Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install        - Install all dependencies (backend + frontend)"
	@echo "  make dev            - Start both backend and frontend servers"
	@echo "  make run-backend    - Start only Django backend server"
	@echo "  make run-frontend   - Start only React frontend server"
	@echo "  make test           - Run backend tests"
	@echo "  make migrate        - Run Django migrations"
	@echo "  make populate       - Populate database with sample data"
	@echo "  make shell          - Open Django shell"
	@echo "  make clean          - Clean temporary files and caches"
	@echo ""

install:
	@echo "Installing backend dependencies..."
	cd backend && $(PIP) install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && $(NPM) install
	@echo "✓ All dependencies installed!"

dev:
	@./start-servers.sh

run-backend:
	@echo "Starting Django backend server..."
	cd backend && $(PYTHON) manage.py runserver

run-frontend:
	@echo "Starting React frontend server..."
	cd frontend && $(NPM) run dev

test:
	@echo "Running backend tests..."
	cd backend && $(PYTHON) manage.py test

migrate:
	@echo "Running migrations..."
	cd backend && $(PYTHON) manage.py migrate

populate:
	@echo "Populating database with sample data..."
	cd backend && $(PYTHON) manage.py populate_data

shell:
	@echo "Opening Django shell..."
	cd backend && $(PYTHON) manage.py shell

clean:
	@echo "Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf logs/*.log 2>/dev/null || true
	@echo "✓ Cleaned!"
