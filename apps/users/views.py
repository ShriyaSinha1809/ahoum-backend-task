from rest_framework import status, views, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import SignupSerializer, VerifyEmailSerializer, CustomTokenObtainPairSerializer
from .utils import generate_otp, store_otp, send_otp_email, verify_otp_value
from .models import Profile

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class SignupView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = generate_otp()
            store_otp(user.email, otp)
            send_otp_email(user.email, otp)
            return Response(
                {"message": "Signup successful. Please verify your email with the OTP sent."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            
            if verify_otp_value(email, otp):
                try:
                    user = User.objects.get(email=email)
                    user.is_active = True
                    user.save()
                    return Response({"message": "Email verified successfully. You can now login."}, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                     return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
            return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
