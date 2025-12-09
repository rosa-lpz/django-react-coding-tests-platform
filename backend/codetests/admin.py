from django.contrib import admin
from .models import Test, TestCase, Submission, CodeProgress

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'time_limit', 'created_at')
    list_filter = ('difficulty', 'created_at')
    search_fields = ('name', 'description')

@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('test', 'is_sample')
    list_filter = ('test', 'is_sample')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'status', 'score', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('user__username', 'test__name')

@admin.register(CodeProgress)
class CodeProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'language', 'updated_at')
    list_filter = ('language', 'updated_at')
    search_fields = ('user__username', 'test__name')

