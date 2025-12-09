# Quick Start Guide

This guide will help you get the Django React Coding Tests Platform up and running in minutes.

## Prerequisites

- Python 3.13+ installed
- Node.js 18+ and npm installed
- Git (optional)

## Step 1: Backend Setup (5 minutes)

### 1.1 Activate Virtual Environment
```bash
source codingtestsvenv/bin/activate
# On Windows: codingtestsvenv\Scripts\activate
```

### 1.2 Navigate to Backend
```bash
cd backend
```

### 1.3 Apply Database Migrations
```bash
python manage.py migrate
```

### 1.4 Create Admin User
```bash
python manage.py createsuperuser
```
Enter username, email, and password when prompted.

### 1.5 Create Sample Tests (Optional)
```bash
python manage.py create_sample_tests
```
This creates 5 sample coding tests with test cases.

### 1.6 Start Backend Server
```bash
python manage.py runserver
```
✅ Backend is now running at **http://localhost:8000**

Keep this terminal open!

## Step 2: Frontend Setup (3 minutes)

### 2.1 Open New Terminal
Open a new terminal window/tab.

### 2.2 Navigate to Frontend
```bash
cd frontend
```

### 2.3 Install Dependencies (if not already done)
```bash
npm install
```

### 2.4 Start Frontend Server
```bash
npm run dev
```
✅ Frontend is now running at **http://localhost:5173**

## Step 3: Test the Application (2 minutes)

### 3.1 Open Browser
Navigate to **http://localhost:5173**

### 3.2 Register Account
1. Click "Register here" link
2. Fill in:
   - Username
   - Email
   - Password
   - Confirm Password
3. Click "Register"

### 3.3 Login
1. Login with your credentials
2. You'll be redirected to the Dashboard

### 3.4 Start a Test
1. Click "Start Test" on any test card
2. You'll enter the Coding Environment with:
   - Problem description on the left
   - Code editor on the right
   - Timer at the top
   - Run Code and Submit buttons

### 3.5 Write and Test Code
1. Write your solution in the editor
2. Click "Run Code" to test
3. See output in the output panel
4. Click "Submit" when ready

### 3.6 Access Admin Panel (Optional)
1. Go to **http://localhost:8000/admin/**
2. Login with superuser credentials
3. Manage tests, view submissions, etc.

## Common Issues

### Backend Port Already in Use
```bash
# Kill process on port 8000 (Linux/Mac)
sudo lsof -ti:8000 | xargs kill -9

# Or use different port
python manage.py runserver 8080
```
Update frontend `src/api/axios.js` to use new port.

### Frontend Port Already in Use
```bash
# Vite will automatically suggest another port
# Or specify port
npm run dev -- --port 3000
```

### Import Errors in IDE
The `rest_framework_simplejwt` import errors in IDE are false positives. The package is installed and works correctly. This is a Pylance/IntelliSense limitation.

### CORS Errors
Make sure Django backend has:
```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
```

## Testing Code Execution

### Example Python Code (Two Sum test):
```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Test
nums = [2, 7, 11, 15]
target = 9
print(two_sum(nums, target))
```

## Project URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api
- **Django Admin**: http://localhost:8000/admin
- **API Tests Endpoint**: http://localhost:8000/api/tests/

## Next Steps

1. ✅ Create more tests via admin panel
2. ✅ Add more test cases (sample and hidden)
3. ✅ Customize test difficulty and time limits
4. ✅ Monitor submissions and candidate performance
5. ✅ Explore the code editor features

## Features to Try

- ✅ Auto-save (code saves every 30 seconds)
- ✅ Multi-language support (Python, JavaScript, Java, C++)
- ✅ Real-time timer
- ✅ Code execution
- ✅ Submission scoring
- ✅ Sample test cases in problem description

## Stopping the Servers

### Stop Backend
Press `Ctrl+C` in the backend terminal

### Stop Frontend
Press `Ctrl+C` in the frontend terminal

### Deactivate Virtual Environment
```bash
deactivate
```

## Ready to Code! 🚀

You're all set! Start creating tests, inviting candidates, and conducting coding interviews.

For detailed documentation, see:
- [Frontend README](frontend/README.md)
- [Backend README](backend/BACKEND_README.md)
- [Main README](README.md)
