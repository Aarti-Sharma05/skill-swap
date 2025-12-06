from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank= True, null=True)
    location = models.TextField(max_length=100,blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    interest = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.user.username
    
class Skills(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=100,blank=True,null=True)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class TeachingSkills(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='teaching_skill')
    skill = models.ForeignKey(Skills,on_delete=models.CASCADE)
    experience_level = models.CharField(
        max_length=50,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('expert', 'Expert'),
        ]
    )
    years_of_experience = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)], blank = False, null = False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['user','skill'],name= 'unique_skill_per_user',violation_error_message='Skill already selected')
        ]

    def __str__(self):
        return f"{self.user.username} teaches {self.skill.name}"
    
class LearningSkills(models.Model):
    LEARNING_MODES = [
        ('online_meeting', 'Online Meeting (1:1)'),
        ('courses', 'Courses / Bootcamps'),
        ('youtube_videos', 'YouTube Videos / Tutorials'),
        ('books', 'Books / PDFs'),
        ('community', 'Community / Group Learning'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='learning_skill')
    skills = models.ForeignKey(Skills,on_delete=models.CASCADE)
    level = models.CharField(
        max_length=50,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('expert', 'Expert'),
        ]
    )
    prefered_learning = models.CharField(max_length=50,choices=LEARNING_MODES,default = 'online_meeting')
    availability = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Learner’s available days/times (e.g., weekends, evenings)"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['user','skills'],name= 'unique_learning_skill_per_user',violation_error_message='Skill already selected')
        ]

    def __str__(self):
        return f"{self.user.username} wants to learn {self.skills.name}"