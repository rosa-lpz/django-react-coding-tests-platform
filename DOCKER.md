# Docker Deployment Guide

This guide explains how to deploy the Coding Tests Platform using Docker and Docker Compose.

## Architecture

The application uses a **single container** architecture with:
- **Multi-stage build**: React frontend is built in Node.js stage, then copied to Python runtime
- **Django + React**: Backend serves API + pre-built React frontend from static files
- **PostgreSQL**: Separate database container with persistent volume
- **Gunicorn**: Production WSGI server (4 workers)
- **Nginx-ready**: Static files served via Django, can add Nginx reverse proxy later

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

## Quick Start

### 1. Configure Environment Variables

Copy the example environment file and customize it:

```bash
cp .env.docker.example .env.docker
```

Edit `.env.docker` and set your values:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database Settings
POSTGRES_DB=coding_platform
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password-here
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:your-secure-password-here@db:5432/coding_platform

# Superuser Settings (optional - for initial setup)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin123

# Application Settings
POPULATE_SAMPLE_DATA=true
CORS_ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

**⚠️ Security Warning**: 
- Change the `SECRET_KEY` to a random string in production
- Use strong passwords for database and superuser
- Set `DEBUG=False` in production
- Specify exact domains in `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`

### 2. Build and Run

Build the Docker images and start the containers:

```bash
docker-compose up --build
```

Or run in detached mode:

```bash
docker-compose up -d --build
```

### 3. Access the Application

Once the containers are running:

- **Application**: http://localhost:8000
- **API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/

**Default Credentials** (if `POPULATE_SAMPLE_DATA=true`):
- Admin: username=`admin`, password=from `DJANGO_SUPERUSER_PASSWORD`
- Test User: username=`testuser`, password=`testpass123`

## Docker Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f db
```

### Stop Containers

```bash
docker-compose down
```

### Stop and Remove Volumes (⚠️ deletes database data)

```bash
docker-compose down -v
```

### Restart Containers

```bash
docker-compose restart
```

### Execute Commands in Container

```bash
# Open shell in web container
docker-compose exec web bash

# Run Django management commands
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput

# Run tests
docker-compose exec web python manage.py test
```

## Application Structure in Container

```
/app/
├── backend/              # Django backend
│   ├── manage.py
│   ├── coding_platform/  # Django project
│   ├── codetests/        # Code tests app
│   ├── users/            # Users app
│   └── staticfiles/      # Collected static files (includes React build)
│       └── index.html    # React app entry point
├── frontend/             # React source (for reference only)
└── docker-entrypoint.sh  # Container startup script
```

## Build Process

The Dockerfile uses a **multi-stage build**:

### Stage 1: Build React Frontend
```dockerfile
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build
# Output: frontend/dist/ (React production build)
```

### Stage 2: Python Runtime
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY backend/requirements.txt backend/requirements.docker.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r requirements.docker.txt
COPY backend/ backend/
COPY --from=frontend-builder /app/frontend/dist backend/staticfiles/
# Serve React app as Django static files
```

## Environment Variables Reference

### Django Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | (insecure) | Django secret key for cryptographic signing |
| `DEBUG` | `False` | Enable debug mode (set to `False` in production) |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated list of allowed hosts |

### Database Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_DB` | `coding_platform` | PostgreSQL database name |
| `POSTGRES_USER` | `postgres` | PostgreSQL username |
| `POSTGRES_PASSWORD` | `postgres` | PostgreSQL password |
| `POSTGRES_HOST` | `db` | PostgreSQL host (service name) |
| `POSTGRES_PORT` | `5432` | PostgreSQL port |
| `DATABASE_URL` | (auto) | Full database connection URL |

### Application Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SUPERUSER_USERNAME` | `admin` | Initial superuser username |
| `DJANGO_SUPERUSER_EMAIL` | `admin@example.com` | Initial superuser email |
| `DJANGO_SUPERUSER_PASSWORD` | `admin123` | Initial superuser password |
| `POPULATE_SAMPLE_DATA` | `true` | Create sample test data on startup |
| `CORS_ALLOWED_ORIGINS` | (localhost) | Comma-separated list of allowed CORS origins |

## Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker-compose logs web
```

**Common issues:**
- Database not ready: Entrypoint script waits for PostgreSQL with retries
- Port 8000 already in use: Change port in `docker-compose.yml`
- Missing environment variables: Check `.env.docker` file

### Database Connection Issues

**Test database connectivity:**
```bash
docker-compose exec web python manage.py dbshell
```

**Reset database:**
```bash
docker-compose down -v
docker-compose up --build
```

### Static Files Not Loading

**Recollect static files:**
```bash
docker-compose exec web python manage.py collectstatic --noinput
docker-compose restart web
```

### Frontend Not Updating

**Rebuild frontend:**
```bash
# Stop containers
docker-compose down

# Rebuild with --no-cache to force fresh build
docker-compose build --no-cache web

# Start containers
docker-compose up -d
```

### Permission Issues

**Fix file permissions:**
```bash
docker-compose exec web chown -R root:root /app
```

## Production Deployment

For production deployments, consider these additional steps:

### 1. Security Hardening

- [ ] Generate strong `SECRET_KEY`: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- [ ] Set `DEBUG=False`
- [ ] Use strong database password
- [ ] Specify exact domains in `ALLOWED_HOSTS`
- [ ] Limit `CORS_ALLOWED_ORIGINS` to your frontend domain
- [ ] Use HTTPS (add Nginx reverse proxy with SSL certificate)
- [ ] Enable Django's security middleware settings

### 2. Add Nginx Reverse Proxy

Create `nginx.conf`:

```nginx
upstream django {
    server web:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /app/backend/staticfiles/;
    }
}
```

Add to `docker-compose.yml`:

```yaml
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/backend/staticfiles
    depends_on:
      - web
```

### 3. Backup Database

```bash
# Backup
docker-compose exec db pg_dump -U postgres coding_platform > backup.sql

# Restore
docker-compose exec -T db psql -U postgres coding_platform < backup.sql
```

### 4. Monitoring

Consider adding:
- Container health checks (already included for database)
- Log aggregation (ELK stack, Grafana Loki)
- Application monitoring (Sentry, New Relic)
- Resource monitoring (Prometheus, Grafana)

## Performance Tuning

### Gunicorn Workers

Adjust workers in `docker-entrypoint.sh`:

```bash
# Formula: (2 × CPU cores) + 1
gunicorn --workers 4 --bind 0.0.0.0:8000 coding_platform.wsgi:application
```

### Database Connection Pooling

Add to `backend/coding_platform/settings.py`:

```python
DATABASES = {
    'default': {
        # ... existing config ...
        'CONN_MAX_AGE': 600,  # Persistent connections for 10 minutes
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}
```

### Static File Caching

For production, serve static files through Nginx with caching headers.

## Development vs Production

| Aspect | Development (local) | Production (Docker) |
|--------|---------------------|---------------------|
| Frontend | Vite dev server (port 5173) | Pre-built, served by Django |
| Backend | Django dev server (port 8000) | Gunicorn WSGI server |
| Database | SQLite | PostgreSQL |
| Debug | `DEBUG=True` | `DEBUG=False` |
| CORS | Allow all origins | Specific origins only |
| Hot Reload | Yes (Vite HMR) | No (static build) |

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Deploy

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker-compose build
      - name: Run tests
        run: docker-compose run web python manage.py test
      - name: Deploy
        run: |
          # Your deployment commands here
```

## Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/configure.html)
- [PostgreSQL Docker Guide](https://hub.docker.com/_/postgres)

## Support

For issues related to:
- **Application bugs**: Check application logs in `logs/` directory
- **Docker issues**: Check `docker-compose logs`
- **Database issues**: Check `docker-compose logs db`
- **Build issues**: Try `docker-compose build --no-cache`
