from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication  # Added import for JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomUserSerializer, ChangePasswordSerializer, ResetPasswordSerializer
import random
from django.contrib.auth import get_user_model
from django.contrib.auth import logout

User = get_user_model()

def send_otp(email, otp):
    subject = "Your OTP for verification"
    message = f"Your OTP code is {otp}."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

class RegisterView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.is_email_verified = False
            user.save()
            send_otp(user.email, otp)
            return Response({
                "message": "User registered successfully. Please verify your email.",
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOtpView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        otp = request.data.get("otp")
        try:
            user = User.objects.get(id=user_id)
            if user.otp == otp:
                user.is_email_verified = True
                user.otp = None
                user.save()
                return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

class ProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        data = request.data
        
        # Check if required fields are provided
        missing_fields = [field for field in ["first_name", "last_name", "address"] if field not in data]
        if missing_fields:
            return Response(
                {"error": f"Missing required fields: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update fields if they are all provided
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.address = data["address"]
        
        # Update password if provided
        if "password" in data:
            user.set_password(data["password"])
        
        user.save()
        return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "Profile deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        
class ChangePasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data["new_password"])
            request.user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()
            send_otp(email, otp)
            return Response({"message": "OTP sent for password reset"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data["user_id"]
            otp = serializer.validated_data["otp"]
            new_password = serializer.validated_data["new_password"]
            try:
                user = User.objects.get(id=user_id, otp=otp)
                user.set_password(new_password)
                user.otp = None  # Clear OTP after resetting password
                user.save()
                return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "Invalid OTP or user not found"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ObtainTokenPairView(APIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(email=request.data.get("email")).first()
        if user and not user.is_email_verified:
            return Response({"error": "Email is not verified"}, status=status.HTTP_403_FORBIDDEN)
        
        # Generate tokens manually if email is verified
        if user and user.check_password(request.data.get("password")):
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class ValidateTokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)
