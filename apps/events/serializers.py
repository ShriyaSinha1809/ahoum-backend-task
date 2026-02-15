from rest_framework import serializers
from .models import Event, Enrollment

class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.email')
    
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by')

class EnrollmentSerializer(serializers.ModelSerializer):
    event_title = serializers.ReadOnlyField(source='event.title')
    
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ('seeker', 'status', 'created_at')

class EventDashboardSerializer(serializers.ModelSerializer):
    enrollments_count = serializers.IntegerField(source='enrollment_count')
    
    class Meta:
        model = Event
        fields = ('id', 'title', 'enrollments_count')
