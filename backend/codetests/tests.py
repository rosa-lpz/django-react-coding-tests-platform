from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Test, TestCase as CodeTestCase, Submission, CodeProgress

User = get_user_model()


class TestModelTestCase(TestCase):
    """Test cases for Test model"""
    
    def setUp(self):
        self.test = Test.objects.create(
            name='Sample Test',
            description='This is a sample test',
            time_limit=30,
            difficulty='Easy'
        )
    
    def test_test_creation(self):
        """Test that a test can be created"""
        self.assertEqual(self.test.name, 'Sample Test')
        self.assertEqual(self.test.difficulty, 'Easy')
        self.assertEqual(self.test.time_limit, 30)
    
    def test_test_str(self):
        """Test the string representation of Test"""
        self.assertEqual(str(self.test), 'Sample Test')


class TestCaseModelTestCase(TestCase):
    """Test cases for TestCase model"""
    
    def setUp(self):
        self.test = Test.objects.create(
            name='Sample Test',
            description='Sample description',
            time_limit=30,
            difficulty='Easy'
        )
        self.test_case = CodeTestCase.objects.create(
            test=self.test,
            input_data='5',
            expected_output='25',
            is_sample=True
        )
    
    def test_testcase_creation(self):
        """Test that a test case can be created"""
        self.assertEqual(self.test_case.input_data, '5')
        self.assertEqual(self.test_case.expected_output, '25')
        self.assertTrue(self.test_case.is_sample)
    
    def test_testcase_relationship(self):
        """Test the relationship between Test and TestCase"""
        self.assertEqual(self.test_case.test, self.test)
        self.assertEqual(self.test.test_cases.count(), 1)


class AuthenticationTestCase(TestCase):
    """Test cases for user authentication"""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
    
    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user_id', response.data)
        self.assertTrue(User.objects.filter(username='testuser').exists())
    
    def test_user_login(self):
        """Test user login"""
        # First create a user
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Try to login
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        login_data = {
            'username': 'wronguser',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


class TestAPITestCase(TestCase):
    """Test cases for Test API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.test = Test.objects.create(
            name='Two Sum',
            description='Find two numbers that add up to target',
            time_limit=30,
            difficulty='Easy'
        )
        
        self.test_case = CodeTestCase.objects.create(
            test=self.test,
            input_data='[2,7,11,15]\n9',
            expected_output='[0, 1]',
            is_sample=True
        )
    
    def test_get_all_tests(self):
        """Test retrieving all tests"""
        response = self.client.get('/api/tests/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Two Sum')
    
    def test_get_single_test(self):
        """Test retrieving a single test"""
        response = self.client.get(f'/api/tests/{self.test.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Two Sum')
        self.assertIn('test_cases', response.data)
    
    def test_get_test_cases(self):
        """Test retrieving test cases for a test"""
        response = self.client.get(f'/api/tests/{self.test.id}/testcases/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['input_data'], '[2,7,11,15]\n9')
    
    def test_unauthorized_access(self):
        """Test that unauthenticated users cannot access tests"""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/tests/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SubmissionTestCase(TestCase):
    """Test cases for code submission"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.test = Test.objects.create(
            name='Simple Output',
            description='Print Hello World',
            time_limit=30,
            difficulty='Easy'
        )
        
        self.test_case = CodeTestCase.objects.create(
            test=self.test,
            input_data='',
            expected_output='Hello World',
            is_sample=True
        )
    
    def test_submit_code(self):
        """Test code submission"""
        code_data = {
            'code': 'print("Hello World")',
            'language': 'python'
        }
        response = self.client.post(
            f'/api/tests/{self.test.id}/submit/',
            code_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('score', response.data)
        self.assertIn('status', response.data)
        
        # Check that submission was created
        self.assertTrue(Submission.objects.filter(user=self.user, test=self.test).exists())


class CodeProgressTestCase(TestCase):
    """Test cases for code progress saving"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.test = Test.objects.create(
            name='Test Problem',
            description='Solve this problem',
            time_limit=30,
            difficulty='Medium'
        )
    
    def test_save_code_progress(self):
        """Test saving code progress"""
        code_data = {
            'code': 'def solution():\n    pass',
            'language': 'python'
        }
        response = self.client.post(
            f'/api/tests/{self.test.id}/save/',
            code_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that progress was saved
        self.assertTrue(CodeProgress.objects.filter(user=self.user, test=self.test).exists())
    
    def test_retrieve_saved_code(self):
        """Test retrieving saved code"""
        # First save some code
        CodeProgress.objects.create(
            user=self.user,
            test=self.test,
            code='def solution():\n    return True',
            language='python'
        )
        
        response = self.client.get(f'/api/tests/{self.test.id}/saved/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('code', response.data)
        self.assertEqual(response.data['language'], 'python')
    
    def test_update_code_progress(self):
        """Test updating existing code progress"""
        # Save initial code
        CodeProgress.objects.create(
            user=self.user,
            test=self.test,
            code='initial code',
            language='python'
        )
        
        # Update with new code
        code_data = {
            'code': 'updated code',
            'language': 'javascript'
        }
        response = self.client.post(
            f'/api/tests/{self.test.id}/save/',
            code_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that there's still only one progress record (updated, not duplicated)
        self.assertEqual(CodeProgress.objects.filter(user=self.user, test=self.test).count(), 1)
        
        # Verify the code was updated
        progress = CodeProgress.objects.get(user=self.user, test=self.test)
        self.assertEqual(progress.code, 'updated code')
        self.assertEqual(progress.language, 'javascript')


class ExecuteCodeTestCase(TestCase):
    """Test cases for code execution"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_execute_python_code(self):
        """Test executing Python code"""
        code_data = {
            'code': 'print("Hello from Python")',
            'language': 'python'
        }
        response = self.client.post('/api/tests/execute/', code_data, format='json')
        if response.status_code != status.HTTP_200_OK:
            print(f"Response status: {response.status_code}")
            print(f"Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('output', response.data)
    
    def test_execute_code_with_error(self):
        """Test executing code with syntax error"""
        code_data = {
            'code': 'print("Missing closing quote)',
            'language': 'python'
        }
        response = self.client.post('/api/tests/execute/', code_data, format='json')
        # Should still return 200 but with error in response
        self.assertIn('error', response.data)
    
    def test_execute_without_code(self):
        """Test executing without providing code"""
        code_data = {
            'language': 'python'
        }
        response = self.client.post('/api/tests/execute/', code_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
