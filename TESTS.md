# Test Suite Documentation

## Backend Tests (Django)

### Overview
Comprehensive test suite covering all major functionality of the coding tests platform backend.

### Test Statistics
- **Total Tests**: 29
- **Status**: ✅ All Passing
- **Coverage Areas**: Models, Authentication, API Endpoints, Code Execution

---

## Test Breakdown

### 1. **codetests.tests** (19 tests)

#### Model Tests
- **TestModelTestCase** (2 tests)
  - ✅ `test_test_creation` - Verify Test model creation
  - ✅ `test_test_str` - Verify Test string representation

- **TestCaseModelTestCase** (2 tests)
  - ✅ `test_testcase_creation` - Verify TestCase model creation
  - ✅ `test_testcase_relationship` - Verify Test-TestCase relationship

#### Authentication Tests
- **AuthenticationTestCase** (3 tests)
  - ✅ `test_user_registration` - Register new users
  - ✅ `test_user_login` - Valid login with JWT tokens
  - ✅ `test_invalid_login` - Handle invalid credentials

#### API Tests
- **TestAPITestCase** (4 tests)
  - ✅ `test_get_all_tests` - Retrieve all tests
  - ✅ `test_get_single_test` - Retrieve specific test
  - ✅ `test_get_test_cases` - Retrieve test cases
  - ✅ `test_unauthorized_access` - Block unauthenticated requests

#### Submission Tests
- **SubmissionTestCase** (1 test)
  - ✅ `test_submit_code` - Submit code and create submission record

#### Code Progress Tests
- **CodeProgressTestCase** (4 tests)
  - ✅ `test_save_code_progress` - Save user's code
  - ✅ `test_retrieve_saved_code` - Retrieve saved code
  - ✅ `test_update_code_progress` - Update existing progress
  - ✅ Verify no duplicate progress records

#### Code Execution Tests
- **ExecuteCodeTestCase** (3 tests)
  - ✅ `test_execute_python_code` - Execute valid Python code
  - ✅ `test_execute_code_with_error` - Handle syntax errors
  - ✅ `test_execute_without_code` - Validate required parameters

---

### 2. **users.tests** (10 tests)

#### User Model Tests
- **CustomUserModelTestCase** (2 tests)
  - ✅ `test_create_user` - Create regular user
  - ✅ `test_create_superuser` - Create admin user

#### Registration Tests
- **UserRegistrationTestCase** (3 tests)
  - ✅ `test_register_user_success` - Successful registration
  - ✅ `test_register_duplicate_username` - Handle duplicates
  - ✅ `test_register_missing_fields` - Validate required fields

#### Login Tests
- **UserLoginTestCase** (4 tests)
  - ✅ `test_login_success` - Valid login returns JWT tokens
  - ✅ `test_login_wrong_password` - Reject wrong password
  - ✅ `test_login_nonexistent_user` - Handle non-existent users
  - ✅ `test_login_missing_credentials` - Validate credentials

#### Current User Tests
- **CurrentUserTestCase** (2 tests)
  - ✅ `test_get_current_user_authenticated` - Return user data when authenticated
  - ✅ `test_get_current_user_unauthenticated` - Block unauthenticated access

---

## Running Tests

### Run All Tests
```bash
cd backend
python manage.py test
```

### Run Specific App Tests
```bash
# Test codetests app only
python manage.py test codetests

# Test users app only
python manage.py test users
```

### Run Specific Test Case
```bash
python manage.py test codetests.tests.TestAPITestCase
```

### Run Single Test
```bash
python manage.py test codetests.tests.TestAPITestCase.test_get_all_tests
```

### Verbose Output
```bash
python manage.py test --verbosity=2
```

---

## Test Coverage

### Models
- ✅ CustomUser model
- ✅ Test model
- ✅ TestCase model
- ✅ Submission model
- ✅ CodeProgress model

### API Endpoints
- ✅ `/api/auth/register/` - User registration
- ✅ `/api/auth/login/` - User login (JWT)
- ✅ `/api/auth/me/` - Current user info
- ✅ `/api/tests/` - List all tests
- ✅ `/api/tests/{id}/` - Get specific test
- ✅ `/api/tests/{id}/testcases/` - Get test cases
- ✅ `/api/tests/{id}/submit/` - Submit solution
- ✅ `/api/tests/{id}/save/` - Save code progress
- ✅ `/api/tests/{id}/saved/` - Get saved code
- ✅ `/api/tests/execute/` - Execute code

### Features Tested
- ✅ User authentication (JWT)
- ✅ Permission checking
- ✅ Model relationships
- ✅ Code execution (Python)
- ✅ Progress tracking
- ✅ Submission scoring
- ✅ Error handling
- ✅ Input validation

---

## Key Testing Patterns

### Authentication Testing
```python
# Force authentication for protected endpoints
self.client.force_authenticate(user=self.user)

# Test without authentication
self.client.force_authenticate(user=None)
```

### API Testing
```python
# POST request
response = self.client.post('/api/endpoint/', data, format='json')

# GET request
response = self.client.get('/api/endpoint/')

# Assert status code
self.assertEqual(response.status_code, status.HTTP_200_OK)

# Assert response data
self.assertIn('key', response.data)
```

---

## Notes

- All tests use in-memory SQLite database for speed
- Tests are isolated - each test runs in a transaction that's rolled back
- Code execution tests use actual subprocess calls (not mocked)
- Authentication uses DRF's APIClient with force_authenticate
- Timeout handling is tested for code execution

---

## Future Test Improvements

- [ ] Add test coverage reporting
- [ ] Add integration tests for full user workflows
- [ ] Add performance/load tests
- [ ] Mock subprocess calls for faster execution
- [ ] Add frontend component tests (Jest/React Testing Library)
- [ ] Add E2E tests (Playwright/Cypress)
