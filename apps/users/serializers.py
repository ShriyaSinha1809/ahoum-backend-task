from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
import uuid
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'password', 'role')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        role = validated_data.pop('role')
        email = validated_data['email']
        password = validated_data['password']
        
        # Generate a unique username based on UUID since username is required by Django
        username = f"{uuid.uuid4().hex[:30]}"
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()
        
        Profile.objects.create(user=user, role=role)
        return user

class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # We pass email as username to authenticate because EmailBackend expects it in username or kwargs
            # But standard authenticate passes username=...
            user = authenticate(request=self.context.get('request'), 
                                username=email, password=password)
            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
             raise serializers.ValidationError('Must include "email" and "password".')

        refresh = RefreshToken.for_user(user)

        if not user.is_active:
             raise serializers.ValidationError('User account is disabled.')

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, min_length=6, required=True)
