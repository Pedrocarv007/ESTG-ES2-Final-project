# Deployment Guide

## Prerequisites
- Docker and Docker Compose
- Python 3.8+
- PostgreSQL (for production)

## Development Deployment

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/macOS)
4. Install dependencies: `pip install -r requirements.txt`
5. Set environment variables in `.env` file
6. Initialize database: `flask db upgrade`
7. Run application: `python run.py`

## Production Deployment with Docker

1. Build Docker image: `docker build -t studyhub-ai .`
2. Run with Docker Compose: `docker-compose up -d`
3. The application will be available at `http://localhost:5000`

## Environment Variables

Required environment variables:
- `FLASK_ENV`: development/production
- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: Database connection string
- `OLLAMA_API_URL`: Ollama API endpoint

## Database Migration

For production deployments:
1. `flask db init` (first time only)
2. `flask db migrate -m "Migration message"`
3. `flask db upgrade`