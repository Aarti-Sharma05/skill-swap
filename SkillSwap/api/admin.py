from django.contrib import admin
from .models import Skills, LearningSkills, TeachingSkills, UserProfile

admin.site.register(Skills)
admin.site.register(LearningSkills)
admin.site.register(TeachingSkills)
admin.site.register(UserProfile)