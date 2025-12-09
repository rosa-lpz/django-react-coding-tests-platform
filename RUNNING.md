# Running Both Client and Server

There are multiple ways to run both the Django backend and React frontend simultaneously.

## Method 1: Using the Startup Script (Recommended) ⭐

The easiest way is to use the provided startup script:

```bash
./start-servers.sh
```

This will:
- ✅ Start both Django and React servers
- ✅ Display colored output showing which server each log comes from
- ✅ Show URLs for both servers
- ✅ Automatically stop both servers when you press `Ctrl+C`

**Output Example:**
```
╔════════════════════════════════════════════════════════════╗
║      Django + React Coding Tests Platform (Dev Mode)      ║
╚════════════════════════════════════════════════════════════╝

[1/2] Starting Django backend...
✓ Backend ready at http://localhost:8000

[2/2] Starting React frontend...
✓ Frontend ready at http://localhost:5173

╔════════════════════════════════════════════════════════════╗
║                    🚀 Servers Running!                     ║
╠════════════════════════════════════════════════════════════╣
║  Backend (Django):  http://localhost:8000                  ║
║  Frontend (React):  http://localhost:5173                  ║
║  Admin Panel:       http://localhost:8000/admin            ║
╠════════════════════════════════════════════════════════════╣
║  Test User: testuser / testpass123                         ║
╠════════════════════════════════════════════════════════════╣
║  Press Ctrl+C to stop both servers                         ║
╚════════════════════════════════════════════════════════════╝
```

---

## Method 2: Using Makefile Commands

If you have `make` installed:

```bash
# Start both servers
make dev

# Or individual servers
make run-backend    # Django only
make run-frontend   # React only
```

See all available commands:
```bash
make help
```

---

## Method 3: Using Separate Terminals

### Terminal 1 - Backend (Django)
```bash
cd backend
source ../codingtestsvenv/bin/activate  # Linux/Mac
# OR
..\codingtestsvenv\Scripts\activate     # Windows

python manage.py runserver
```

### Terminal 2 - Frontend (React)
```bash
cd frontend
npm run dev
```

---

## Method 4: Using tmux (Advanced)

If you have tmux installed:

```bash
# Create a new tmux session with split panes
tmux new-session -d -s devservers
tmux split-window -h
tmux send-keys -t devservers:0.0 'cd backend && ../codingtestsvenv/bin/python manage.py runserver' C-m
tmux send-keys -t devservers:0.1 'cd frontend && npm run dev' C-m
tmux attach -t devservers
```

---

## Method 5: Using Screen (Alternative to tmux)

```bash
# Start backend in background screen
screen -dmS backend bash -c 'cd backend && ../codingtestsvenv/bin/python manage.py runserver'

# Start frontend in background screen
screen -dmS frontend bash -c 'cd frontend && npm run dev'

# View backend logs
screen -r backend

# View frontend logs  
screen -r frontend

# List all screens
screen -ls

# Stop servers
screen -X -S backend quit
screen -X -S frontend quit
```

---

## Access Points

Once both servers are running:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:5173 | React application (main interface) |
| **Backend API** | http://localhost:8000/api | Django REST API endpoints |
| **Admin Panel** | http://localhost:8000/admin | Django admin interface |

---

## Default Credentials

- **Test User**: `testuser` / `testpass123`
- **Admin User**: Create with `python manage.py createsuperuser`

---

## Stopping the Servers

### If using start-servers.sh or Makefile:
- Press `Ctrl+C` once - it will gracefully stop both servers

### If using separate terminals:
- Press `Ctrl+C` in each terminal

### If using tmux:
- Press `Ctrl+B` then `&` to kill the session
- Or exit each pane with `Ctrl+D`

### If using screen:
```bash
screen -X -S backend quit
screen -X -S frontend quit
```

---

## Troubleshooting

### Port Already in Use

**Backend (Port 8000):**
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
# Or
fuser -k 8000/tcp
```

**Frontend (Port 5173):**
```bash
# Find and kill process
lsof -ti:5173 | xargs kill -9
# Or
fuser -k 5173/tcp
```

### Virtual Environment Not Found
```bash
# Recreate virtual environment
python3 -m venv codingtestsvenv
source codingtestsvenv/bin/activate
pip install -r backend/requirements.txt
```

### Frontend Dependencies Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## Development Workflow

1. **First Time Setup:**
   ```bash
   # Install dependencies
   make install
   
   # Run migrations
   make migrate
   
   # Create sample data
   make populate
   ```

2. **Daily Development:**
   ```bash
   # Start both servers
   make dev
   # Or
   ./start-servers.sh
   ```

3. **Testing:**
   ```bash
   # Run tests
   make test
   ```

---

## Tips

- 💡 Use `start-servers.sh` for the best development experience
- 💡 Logs are prefixed with `[Backend]` or `[Frontend]` for easy identification
- 💡 The script automatically handles cleanup when you stop with Ctrl+C
- 💡 Both servers support hot-reloading - changes will refresh automatically
