from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile,TeachingSkills,Skills,LearningSkills

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','is_staff','password','is_active']
        extra_kwargs = {'password' : {'write_only' : True}}

    
    def create(self,validated_data):
        '''Create serializers validating data'''
        user = User.objects.create_user(
            username=validated_data["username"],
            is_staff = validated_data['is_staff'],
            is_active = validated_data['is_active'],
            email=validated_data['email'],
            password= validated_data['password']
        )
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'

class TeachingSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingSkills
        fields = '__all__'

    def validate_stars(self,value):
        if value<1 or value>5:
            raise serializers.ValidationError("Rating must be between 1 to 5 stars")
        return value

class LearningSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningSkills
        fields = '__all__'
