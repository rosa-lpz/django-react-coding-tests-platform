# Coding Tests Platform - Backend

Django REST Framework backend for the coding tests platform with JWT authentication and code execution capabilities.

## Updated Models

### Users App

#### CustomUser Model
```python
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Extends Django's default user model
    # Custom fields can be added as needed
```

### Codetests App

#### Test Model
```python
class Test(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    time_limit = models.IntegerField()  # in minutes
    difficulty = models.CharField(
        max_length=50, 
        choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### TestCase Model
```python
class TestCase(models.Model):
    test = models.ForeignKey(Test, related_name='test_cases', on_delete=models.CASCADE)
    input_data = models.TextField()
    expected_output = models.TextField()
    is_sample = models.BooleanField(default=False)  # Show as sample to users
```

#### Submission Model
```python
class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='submissions')
    code = models.TextField()
    language = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('passed', 'Passed'), ('failed', 'Failed')]
    )
    score = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
```

#### CodeProgress Model
```python
class CodeProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='code_progress')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='code_progress')
    code = models.TextField()
    language = models.CharField(max_length=50, default='python')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'test')
```

## API Endpoints

### Authentication (`/api/users/`)
- `POST /register/` - Register new user
- `POST /login/` - Login and get JWT tokens
- `GET /me/` - Get current user info (requires auth)

### Tests (`/api/tests/`)
- `GET /` - List all tests
- `GET /:id/` - Get test details
- `GET /:id/testcases/` - Get test cases for a test
- `POST /:id/submit/` - Submit code solution
- `POST /execute/` - Execute code (for testing)
- `POST /:id/save/` - Save code progress
- `GET /:id/saved/` - Get saved code progress

## Serializers

### TestSerializer
```python
class TestSerializer(serializers.ModelSerializer):
    test_cases = TestCaseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Test
        fields = ['id', 'name', 'description', 'time_limit', 'difficulty', 'test_cases', 'created_at']
```

### SubmissionSerializer
```python
class SubmissionSerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(source='test.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Submission
        fields = ['id', 'user', 'username', 'test', 'test_name', 'code', 'language', 
                  'status', 'score', 'submitted_at']
```

## Running Migrations

After updating the models, run:

```bash
cd backend
source ../codingtestsvenv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

## Creating Sample Data

Use Django admin or create a management command:

```python
# In codetests/management/commands/create_sample_tests.py
from django.core.management.base import BaseCommand
from codetests.models import Test, TestCase

class Command(BaseCommand):
    def handle(self, *args, **options):
        test = Test.objects.create(
            name="Two Sum",
            description="Given an array of integers, return indices of two numbers that add up to a target.",
            time_limit=30,
            difficulty="Easy"
        )
        
        TestCase.objects.create(
            test=test,
            input_data="[2, 7, 11, 15]\n9",
            expected_output="[0, 1]",
            is_sample=True
        )
```

Run with:
```bash
python manage.py create_sample_tests
```

## Admin Panel

Access at http://localhost:8000/admin/

All models are registered in admin:
- Tests management
- Test cases management
- Submissions viewing
- Code progress tracking

## Security Notes

- JWT tokens expire after configured time
- Code execution is sandboxed (subprocess with timeout)
- CORS configured for frontend origin
- Django REST Framework permissions on all endpoints

## Code Execution

The backend executes user code in a subprocess with timeout:

```python
def execute_code(self, code, input_data, language):
    try:
        if language == 'python':
            process = subprocess.Popen(
                ['python3', '-c', code],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5
            )
            output, errors = process.communicate(input=input_data.encode())
            return output.decode()
    except subprocess.TimeoutExpired:
        return "Error: Execution timeout"
```

⚠️ **Note:** For production, consider using Docker containers or a sandboxed environment for code execution.

## Next Steps

1. Implement more language support (Java, C++, JavaScript)
2. Add Docker-based code execution for better security
3. Implement rate limiting
4. Add submission history
5. Create leaderboards
6. Add real-time test monitoring for admins
