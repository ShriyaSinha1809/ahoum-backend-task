from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'my-enrollments', EnrollmentViewSet, basename='my-enrollments')

urlpatterns = [
    path('', include(router.urls)),
]
