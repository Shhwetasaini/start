from django.urls import path
#from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    VerifyOtpView,
    LogoutView,
    ProfileView,
    ChangePasswordView,
    ResetPasswordView,
    ObtainTokenPairView,
    ValidateTokenView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify_otp'),
    path('login/', ObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('token/validate/', ValidateTokenView.as_view(), name='validate_token'),
    
]
