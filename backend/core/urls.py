from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ApiRegisterView, ApiProfileView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='obtain-token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('register/', ApiRegisterView.as_view(), name='register-api'),
    path('profile/', ApiProfileView.as_view(), name='profile-api'),
]
