from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Test(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    time_limit = models.IntegerField()  # Time limit in minutes
    difficulty = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES, default='Medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class TestCase(models.Model):
    test = models.ForeignKey(Test, related_name='test_cases', on_delete=models.CASCADE)
    input_data = models.TextField()
    expected_output = models.TextField()
    is_sample = models.BooleanField(default=False)  # Whether to show as sample

    def __str__(self):
        return f"Test case for {self.test.name}"

class Submission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='submissions')
    code = models.TextField()
    language = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    score = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.test.name}"

class CodeProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='code_progress')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='code_progress')
    code = models.TextField()
    language = models.CharField(max_length=50, default='python')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'test')
    
    def __str__(self):
        return f"{self.user.username} - {self.test.name} progress"
