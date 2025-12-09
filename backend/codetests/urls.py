from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestViewSet, ExecuteCodeView

router = DefaultRouter()
router.register(r'tests', TestViewSet, basename='test')

urlpatterns = [
    path('', include(router.urls)),
    path('tests/execute/', ExecuteCodeView.as_view(), name='execute_code'),
]

