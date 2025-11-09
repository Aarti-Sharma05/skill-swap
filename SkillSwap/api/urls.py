from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import Signup,update_profile,get_profile

urlpatterns = [
    path('auth/login/',TokenObtainPairView.as_view(),name='login'),
    path('auth/refresh-token/',TokenRefreshView.as_view(),name='refresh-token'),
    path('auth/signup/',Signup,name = 'signup'),
    path('auth/update-profile/<int:id>/', update_profile, name = 'profile-update'),
    path('auth/profile/<int:id>/',get_profile,name = 'get-profile')
]