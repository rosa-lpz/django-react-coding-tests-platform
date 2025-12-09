#!/bin/bash
set -e

echo "Starting Django + React Coding Tests Platform..."

# Wait for database if DB_HOST is set
if [ -n "$DB_HOST" ]; then
    echo "Waiting for database at $DB_HOST:${DB_PORT:-5432}..."
    while ! nc -z $DB_HOST ${DB_PORT:-5432}; do
        sleep 0.5
    done
    echo "Database is ready!"
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files (including React build)
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if specified
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser..."
    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print('Superuser created.')
else:
    print('Superuser already exists.')
END
fi

# Populate sample data if specified
if [ "$POPULATE_SAMPLE_DATA" = "true" ]; then
    echo "Populating sample data..."
    python manage.py populate_data || echo "Sample data already exists or failed to populate"
fi

# Start Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn coding_platform.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS:-4} \
    --threads ${GUNICORN_THREADS:-2} \
    --timeout 120 \
    --access-logfile /app/logs/access.log \
    --error-logfile /app/logs/error.log \
    --log-level info
