from django.shortcuts import get_object_or_404
from .models import UserProfile,Skills,TeachingSkills,LearningSkills
from django.contrib.auth.models import User
from django.db.models import Prefetch

def get_user_by_id(id):
    return get_object_or_404(UserProfile,user__id=id)

def get_skill_object():
    return Skills.objects.all()

def get_teaching_skill_object():
    return TeachingSkills.objects.all()

def get_teaching_skill_by_id(id):
    return get_object_or_404(TeachingSkills,id=id)

def get_learning_skill_object():
    return LearningSkills.objects.all()

def get_learning_skill_by_id(id):
    return get_object_or_404(LearningSkills,id=id)

def user_data(user):
    return (
        User.objects.exclude(id=user.id)
        .select_related("profile")   # loads UserProfile in same query
        .prefetch_related(           # load skills efficiently
            Prefetch(
                "learning_skill",
                queryset=LearningSkills.objects.select_related("skills")
            ),
            Prefetch(
                "teaching_skill",
                queryset=TeachingSkills.objects.select_related("skill")
            )
        )
    )