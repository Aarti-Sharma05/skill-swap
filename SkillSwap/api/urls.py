from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import Signup,Profile,Skill,LearnSkill,TeachSkill,home

urlpatterns = [
    path('auth/login/',TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh-token/',TokenRefreshView.as_view(), name='refresh-token'),
    path('auth/signup/',Signup.as_view(), name = 'signup'),
    path('auth/update-profile/<int:id>/', Profile.as_view(), name = 'profile-update'),
    path('auth/profile/<int:id>/',Profile.as_view(), name = 'get-profile'),
    path('skills/',Skill.as_view(), name= 'skills'),
    path('teach-skills/',TeachSkill.as_view(), name = 'teach-skills'),
    path('learn-skills/',LearnSkill.as_view(), name = 'learn-skills'),
    path('learn-skill/<int:id>/', LearnSkill.as_view(), name = 'learn-skill'),
    path('teach-skill/<int:id>/',TeachSkill.as_view(), name = 'teach-skill'),
    path('home/',home,name= 'home')
]