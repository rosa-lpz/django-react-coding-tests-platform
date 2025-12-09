# Coding Tests Platform - React + Django

A full-stack coding tests platform with user authentication, candidate dashboard, and an interactive coding environment.

## Features

### Frontend (React + Vite)
- ✅ User authentication (Login/Register)
- ✅ Candidate dashboard with available tests
- ✅ Interactive coding environment with Monaco Editor
- ✅ Real-time timer (counts down during tests)
- ✅ Auto-save functionality (saves every 30 seconds)
- ✅ Multiple programming language support (Python, JavaScript, Java, C++)
- ✅ Output display panel
- ✅ Syntax highlighting and error highlighting
- ✅ Responsive design

### Backend (Django + DRF)
- ✅ JWT authentication
- ✅ User management
- ✅ Test and TestCase models
- ✅ Code submission tracking
- ✅ Code progress saving
- ✅ Code execution (Python supported)
- ✅ REST API endpoints

## Project Structure

```
.
├── frontend/                 # React + Vite frontend
│   ├── src/
│   │   ├── api/             # API service layer
│   │   ├── components/      # React components
│   │   ├── context/         # Context providers (Auth)
│   │   ├── pages/           # Page components
│   │   └── App.jsx          # Main app component
│   └── package.json
├── backend/                  # Django backend
│   ├── codetests/           # Tests app
│   │   ├── models.py        # Test, TestCase, Submission, CodeProgress
│   │   ├── views.py         # API views
│   │   ├── serializers.py   # DRF serializers
│   │   └── management/      # Management commands
│   ├── users/               # Users app
│   │   ├── models.py        # CustomUser model
│   │   └── views.py         # Auth views
│   └── manage.py
└── codingtestsvenv/         # Python virtual environment
```

## Setup Instructions

### Backend Setup

1. **Activate virtual environment:**
   ```bash
   source codingtestsvenv/bin/activate  # On Linux/Mac
   # OR
   codingtestsvenv\Scripts\activate  # On Windows
   ```

2. **Navigate to backend:**
   ```bash
   cd backend
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create sample data:**
   ```bash
   python manage.py populate_data
   ```
   This creates:
   - Test user: `testuser` / `testpass123`
   - 4 sample coding tests with test cases

5. **Start Django server:**
   ```bash
   python manage.py runserver
   ```
   Backend will run at: http://localhost:8000

### Frontend Setup

1. **Navigate to frontend:**
   ```bash
   cd frontend
   ```

2. **Install dependencies (if not already installed):**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```
   Frontend will run at: http://localhost:5173

## Usage

1. **Register a new account** or use the test credentials:
   - Username: `testuser`
   testuser@email.com
   - Password: `testpass123`

2. **Browse available tests** on the dashboard

3. **Start a test** and use the coding environment:
   - Write code in the Monaco editor
   - Select your programming language
   - Run your code to test it
   - Code auto-saves every 30 seconds
   - Submit when ready

## API Endpoints

### Authentication
- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - Login and get JWT tokens
- `GET /api/users/me/` - Get current user info

### Tests
- `GET /api/tests/` - Get all tests
- `GET /api/tests/{id}/` - Get specific test
- `GET /api/tests/{id}/testcases/` - Get test cases
- `POST /api/tests/{id}/submit/` - Submit code solution
- `POST /api/tests/{id}/save/` - Save code progress
- `GET /api/tests/{id}/saved/` - Get saved code
- `POST /api/tests/execute/` - Execute code (testing)

## Technologies

### Frontend
- React 19
- Vite
- React Router DOM
- Monaco Editor (VS Code editor)
- Axios

### Backend
- Django 6.0
- Django REST Framework
- djangorestframework-simplejwt
- django-cors-headers

## Security Notes

⚠️ **Important:** Code execution is currently implemented using subprocess and should be properly sandboxed in production. Consider using:
- Docker containers
- Isolated execution environments
- Resource limits
- Timeout mechanisms

## Future Enhancements

- [ ] Support for more programming languages
- [ ] Advanced code execution sandboxing
- [ ] Test result history
- [ ] Leaderboard
- [ ] Admin panel for test creation
- [ ] Code diff viewer
- [ ] Collaborative coding
- [ ] Video proctoring

## License

MIT License
