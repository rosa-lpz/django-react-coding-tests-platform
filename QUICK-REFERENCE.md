# Quick Reference Guide - Coding Tests Platform

## Development Workflow

### Starting the Application

**Local Development (with hot-reload):**
```bash
# Option 1: Using Makefile
make dev

# Option 2: Using script
./start-servers.sh

# Option 3: Manual
cd backend && source ../codingtestsvenv/bin/activate && python manage.py runserver
cd frontend && npm run dev
```

**Docker Production:**
```bash
docker-compose up --build
```

### Stopping the Application

**Local Development:**
```bash
# Option 1: Makefile
make stop

# Option 2: Script
./stop-servers.sh

# Option 3: Ctrl+C in terminal
```

**Docker:**
```bash
docker-compose down
```

## Common Commands

### Backend (Django)

```bash
# Activate virtual environment
source codingtestsvenv/bin/activate

# Run server
cd backend && python manage.py runserver

# Run tests
python manage.py test

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Open Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

### Frontend (React)

```bash
# Install dependencies
cd frontend && npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

### Docker

```bash
# Build and start
docker-compose up --build

# Start in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web
docker-compose logs -f db

# Stop containers
docker-compose down

# Stop and remove volumes (⚠️ deletes database)
docker-compose down -v

# Restart containers
docker-compose restart

# Execute command in container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py test
docker-compose exec web bash

# View running containers
docker-compose ps

# Rebuild without cache
docker-compose build --no-cache
```

### Testing

```bash
# Run all tests
make test

# Run backend tests only
cd backend && python manage.py test

# Run specific test file
python manage.py test codetests.tests

# Run with coverage
python manage.py test --coverage

# In Docker
docker-compose exec web python manage.py test
```

## URLs

### Local Development
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api
- **Admin Panel**: http://localhost:8000/admin
- **API Docs**: http://localhost:8000/api/schema/swagger-ui (if configured)

### Docker Production
- **Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## API Endpoints

### Authentication
```
POST   /api/auth/register/     - Register new user
POST   /api/auth/login/        - Login (get tokens)
POST   /api/auth/token/refresh/ - Refresh access token
GET    /api/auth/user/         - Get current user info
```

### Tests
```
GET    /api/tests/             - List all tests
POST   /api/tests/             - Create test (admin)
GET    /api/tests/{id}/        - Get test details
PUT    /api/tests/{id}/        - Update test (admin)
DELETE /api/tests/{id}/        - Delete test (admin)
POST   /api/tests/{id}/start/  - Start test (get initial code)
```

### Code Execution
```
POST   /api/tests/execute/     - Run code against sample test cases
POST   /api/tests/{id}/submit/ - Submit final solution
POST   /api/tests/{id}/autosave/ - Auto-save progress
```

### Submissions
```
GET    /api/tests/{id}/submissions/ - Get user submissions for test
GET    /api/submissions/       - List all user submissions
```

## Default Credentials

### Test User
- Username: `testuser`
- Password: `testpass123`

### Admin (if created)
- Username: `admin`
- Password: Set during `createsuperuser` or via `DJANGO_SUPERUSER_PASSWORD` env var

## Project Structure

```
.
├── backend/                  # Django backend
│   ├── coding_platform/      # Django project settings
│   ├── codetests/           # Tests app
│   ├── users/               # Users app
│   ├── manage.py
│   └── requirements.txt
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── api/             # API service layer
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── codingtestsvenv/         # Python virtual environment
├── Dockerfile               # Multi-stage Docker build
├── docker-compose.yml       # Docker Compose config
├── .env.docker.example      # Environment template
├── docker-entrypoint.sh     # Container startup script
├── start-servers.sh         # Dev server startup
├── stop-servers.sh          # Dev server shutdown
├── docker-verify.sh         # Docker setup checker
├── Makefile                 # Development commands
├── README.md                # Main documentation
├── RUNNING.md               # Detailed running guide
├── DOCKER.md                # Docker deployment guide
└── SETUP.md                 # Setup instructions
```

## Environment Variables

### Development (.env)
```bash
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Docker Production (.env.docker)
```bash
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:password@db:5432/dbname
POSTGRES_DB=coding_platform
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure-password
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=secure-password
POPULATE_SAMPLE_DATA=true
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Find process using port 5173
lsof -i :5173

# Kill process by PID
kill -9 <PID>
```

### Database Issues
```bash
# Delete database and start fresh
rm backend/db.sqlite3
python manage.py migrate

# In Docker
docker-compose down -v
docker-compose up --build
```

### Docker Build Issues
```bash
# Clean rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Frontend Build Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Backend Dependencies Issues
```bash
source codingtestsvenv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
```

## Makefile Targets

```bash
make dev        # Start both servers
make test       # Run all tests
make clean      # Clean generated files
make setup      # Initial setup
make stop       # Stop servers
make help       # Show help
```

## Git Workflow

```bash
# Check status
git status

# Stage changes
git add .

# Commit
git commit -m "Your message"

# Push
git push origin main

# Pull latest
git pull origin main
```

## Performance Tips

### Development
- Use `make dev` for convenient startup
- Keep both terminals visible for debugging
- Use browser DevTools Network tab for API debugging
- Monaco Editor auto-saves every 30 seconds

### Production
- Set `DEBUG=False` in production
- Use environment variables for sensitive data
- Enable HTTPS with Nginx reverse proxy
- Configure database connection pooling
- Use CDN for static files (if scaling)

## Security Checklist

- [ ] Change `SECRET_KEY` in production
- [ ] Set `DEBUG=False` in production
- [ ] Use strong database passwords
- [ ] Specify exact domains in `ALLOWED_HOSTS`
- [ ] Limit `CORS_ALLOWED_ORIGINS` to frontend domain
- [ ] Enable HTTPS in production
- [ ] Regular security updates for dependencies
- [ ] Review Django security checklist

## Monitoring

### Development
```bash
# Watch logs
tail -f logs/backend.log
tail -f logs/frontend.log

# Check processes
ps aux | grep python
ps aux | grep node
```

### Docker
```bash
# Container stats
docker stats

# Logs
docker-compose logs -f --tail=100

# Health check
docker-compose ps
```

## Documentation

- **README.md** - Overview and features
- **SETUP.md** - Detailed setup guide
- **RUNNING.md** - How to run the application
- **DOCKER.md** - Docker deployment guide
- **QUICK-REFERENCE.md** - This file

## Support Resources

- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- React Documentation: https://react.dev/
- Vite Documentation: https://vitejs.dev/
- Monaco Editor: https://microsoft.github.io/monaco-editor/
- Docker Documentation: https://docs.docker.com/

## Keyboard Shortcuts

### Monaco Editor
- `Ctrl+S` / `Cmd+S` - Save (auto-save enabled)
- `Ctrl+/` / `Cmd+/` - Toggle comment
- `Ctrl+F` / `Cmd+F` - Find
- `Ctrl+H` / `Cmd+H` - Find and replace
- `Alt+Up/Down` - Move line up/down
- `Ctrl+D` / `Cmd+D` - Select next occurrence

### VS Code (for development)
- `Ctrl+`` - Toggle terminal
- `Ctrl+P` - Quick file open
- `Ctrl+Shift+P` - Command palette

## Code Formatting

### Python (Backend)
```bash
# Install black
pip install black

# Format code
black backend/

# Check without formatting
black --check backend/
```

### JavaScript (Frontend)
```bash
# Lint
npm run lint

# Format with prettier (if configured)
npm run format
```

## Database Management

### Backup SQLite (Development)
```bash
cp backend/db.sqlite3 backend/db.sqlite3.backup
```

### Backup PostgreSQL (Docker)
```bash
docker-compose exec db pg_dump -U postgres coding_platform > backup.sql
```

### Restore PostgreSQL (Docker)
```bash
docker-compose exec -T db psql -U postgres coding_platform < backup.sql
```

## Quick Test Scenarios

### 1. Register and Login
1. Navigate to http://localhost:5173
2. Click "Register"
3. Fill form and submit
4. Login with credentials

### 2. Start a Test
1. Login as testuser
2. Click "Start Test" on any test
3. Code editor should open
4. Timer should start counting down

### 3. Run Code
1. Write code in editor
2. Click "Run Code"
3. See output in panel below

### 4. Submit Solution
1. Complete code
2. Click "Submit"
3. See score based on test cases passed

### 5. Admin Panel
1. Navigate to http://localhost:8000/admin
2. Login with superuser credentials
3. Manage tests and view submissions
