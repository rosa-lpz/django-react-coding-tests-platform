from rest_framework import serializers
from .models import Test, TestCase, Submission, CodeProgress

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['id', 'input_data', 'expected_output', 'is_sample']

class TestSerializer(serializers.ModelSerializer):
    test_cases = TestCaseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Test
        fields = ['id', 'name', 'description', 'time_limit', 'difficulty', 'test_cases', 'created_at']

class SubmissionSerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(source='test.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Submission
        fields = ['id', 'user', 'username', 'test', 'test_name', 'code', 'language', 'status', 'score', 'submitted_at']
        read_only_fields = ['user', 'status', 'score', 'submitted_at']

class CodeProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeProgress
        fields = ['id', 'user', 'test', 'code', 'language', 'updated_at']
        read_only_fields = ['user', 'updated_at']

