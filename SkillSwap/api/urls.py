from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import Signup,profile,create_skills,create_teaching_skills,create_learning_skills,fetch_skills,fetch_teaching_skills,fetch_learning_skills
from .views import update_skills,teaching_skills,learning_skills

urlpatterns = [
    path('auth/login/',TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh-token/',TokenRefreshView.as_view(), name='refresh-token'),
    path('auth/signup/',Signup, name = 'signup'),
    path('auth/update-profile/<int:id>/', profile, name = 'profile-update'),
    path('auth/profile/<int:id>/',profile, name = 'get-profile'),
    path('skills/',create_skills, name= 'skills'),
    path('teach-skills/',create_teaching_skills, name = 'teach-skills'),
    path('learn-skills/',create_learning_skills, name = 'learn-skills'),
    path('list/skills/',fetch_skills, name = 'get-skills'),
    path('list/teach-skills/',fetch_teaching_skills, name = 'get-teach-skills'),
    path('list/learn-skill',fetch_learning_skills, name = 'get-learn-skills'),
    path('skill/<int:id>/',update_skills, name = 'skill'),
    path('learn-skill/<int:id>/', learning_skills, name = 'learn-skill'),
    path('teach-skill/<int:id>/',teaching_skills, name = 'teach-skill')
]