from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Test, TestCase, Submission, CodeProgress
from .serializers import TestSerializer, TestCaseSerializer, SubmissionSerializer, CodeProgressSerializer
import subprocess
import json

# Test ViewSet (CRUD for Tests)
class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def testcases(self, request, pk=None):
        """Get test cases for a specific test"""
        test = self.get_object()
        test_cases = TestCase.objects.filter(test=test)
        serializer = TestCaseSerializer(test_cases, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit code for a test"""
        test = self.get_object()
        code = request.data.get('code')
        language = request.data.get('language', 'python')

        # Create submission
        submission = Submission.objects.create(
            user=request.user,
            test=test,
            code=code,
            language=language
        )

        # Run test cases
        test_cases = TestCase.objects.filter(test=test)
        passed_count = 0
        results = []

        for case in test_cases:
            result = self.execute_code(code, case.input_data, language)
            passed = result.strip() == case.expected_output.strip()
            if passed:
                passed_count += 1
            
            results.append({
                'input': case.input_data,
                'expected_output': case.expected_output,
                'actual_output': result,
                'passed': passed
            })

        # Calculate score
        score = int((passed_count / len(test_cases)) * 100) if test_cases else 0
        submission.score = score
        submission.status = 'passed' if score >= 70 else 'failed'
        submission.save()

        return Response({
            'submission_id': submission.id,
            'score': score,
            'status': submission.status,
            'results': results
        })

    @action(detail=True, methods=['post'])
    def save(self, request, pk=None):
        """Save code progress"""
        test = self.get_object()
        code = request.data.get('code')
        language = request.data.get('language', 'python')

        progress, created = CodeProgress.objects.update_or_create(
            user=request.user,
            test=test,
            defaults={'code': code, 'language': language}
        )

        serializer = CodeProgressSerializer(progress)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def saved(self, request, pk=None):
        """Get saved code progress"""
        test = self.get_object()
        try:
            progress = CodeProgress.objects.get(user=request.user, test=test)
            serializer = CodeProgressSerializer(progress)
            return Response(serializer.data)
        except CodeProgress.DoesNotExist:
            return Response({'code': '', 'language': 'python'}, status=status.HTTP_404_NOT_FOUND)

    def execute_code(self, code, input_data, language):
        """Execute code in a subprocess (basic implementation)"""
        try:
            if language == 'python':
                process = subprocess.Popen(
                    ['python3', '-c', code],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                output, errors = process.communicate(input=input_data.encode(), timeout=5)
                if errors:
                    return f"Error: {errors.decode()}"
                return output.decode()
            else:
                return "Language not supported yet"
        except subprocess.TimeoutExpired:
            process.kill()
            return "Error: Execution timeout"
        except Exception as e:
            return f"Error: {str(e)}"


# Execute Code (for testing without submission)
class ExecuteCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Execute code and return output"""
        code = request.data.get('code')
        language = request.data.get('language', 'python')
        test_id = request.data.get('test_id')

        if not code:
            return Response({'error': 'No code provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if language == 'python':
                process = subprocess.Popen(
                    ['python3', '-c', code],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                output, errors = process.communicate(timeout=5)
                
                if errors:
                    return Response({'output': '', 'error': errors.decode()})
                
                return Response({'output': output.decode(), 'error': ''})
            else:
                return Response({'error': 'Language not supported yet'}, status=status.HTTP_400_BAD_REQUEST)
        except subprocess.TimeoutExpired:
            process.kill()
            return Response({'error': 'Execution timeout (5 seconds)'}, status=status.HTTP_408_REQUEST_TIMEOUT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

