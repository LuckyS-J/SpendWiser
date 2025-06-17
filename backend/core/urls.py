from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ApiRegisterView, ApiProfileView, HomeView

urlpatterns = [
    #API
    path('api/token/', TokenObtainPairView.as_view(), name='obtain-token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('api/register/', ApiRegisterView.as_view(), name='register-api'),
    path('api/profile/', ApiProfileView.as_view(), name='profile-api'),

    #FRONTEND
    path('', HomeView.as_view(), name='home-page'),
]
