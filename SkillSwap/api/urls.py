from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import Signup

urlpatterns = [
    path('auth/login/',TokenObtainPairView.as_view(),name='login'),
    path('auth/refresh-token/',TokenRefreshView.as_view(),name='refresh-token'),
    path('auth/signup/',Signup,name = 'signup')
]