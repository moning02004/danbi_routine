from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api_user.views import TokenExpireView, UserRegisterAPIView

urlpatterns = [
    path("", UserRegisterAPIView.as_view()),
    path("/token", TokenObtainPairView.as_view()),
    path("/refresh", TokenRefreshView.as_view()),
    path("/expire", TokenExpireView.as_view()),
]
