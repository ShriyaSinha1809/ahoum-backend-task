from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event, Enrollment
from .serializers import EventSerializer, EnrollmentSerializer, EventDashboardSerializer
from apps.users.permissions import IsSeeker, IsFacilitator, IsOwnerOrReadOnly
from django.utils import timezone
from datetime import timedelta

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['location', 'language']
    search_fields = ['title', 'description']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsFacilitator, IsOwnerOrReadOnly]
        elif self.action in ['enroll']:
            permission_classes = [IsSeeker]
        else:
            permission_classes = [permissions.IsAuthenticated] # Or AllowAny if public
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if self.action == 'list':
            # Seekers see all events (filtered)
            # Facilitators see their own events? Requirement says "CRUD events: Only for their own events".
            # But standard list usually returns all? Let's assume Facilitator GET /events/ returns their own.
            if hasattr(user, 'profile') and user.profile.role == 'FACILITATOR':
                return Event.objects.filter(created_by=user)
            # Seeker sees all future events? Or all events?
            # Requirement: "Filter by ... date range".
            return Event.objects.all()
        return Event.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsSeeker])
    def enroll(self, request, pk=None):
        event = self.get_object()
        seeker = request.user
        
        # Check if already enrolled
        if Enrollment.objects.filter(event=event, seeker=seeker, status='CONFIRMED').exists():
            return Response({"error": "You are already enrolled in this event."}, status=status.HTTP_400_BAD_REQUEST)

        # Check capacity
        if event.enrollments.filter(status='CONFIRMED').count() >= event.capacity:
             return Response({"error": "Event is full."}, status=status.HTTP_400_BAD_REQUEST)

        Enrollment.objects.create(event=event, seeker=seeker)
        return Response({"message": "Enrolled successfully."}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], permission_classes=[IsFacilitator])
    def dashboard(self, request):
        events = Event.objects.filter(created_by=request.user)
        serializer = EventDashboardSerializer(events, many=True)
        return Response(serializer.data)

class EnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsSeeker]

    def get_queryset(self):
        return Enrollment.objects.filter(seeker=self.request.user)
