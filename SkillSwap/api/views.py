from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .models import UserProfile,Skills,TeachingSkills,LearningSkills
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
import io
from .serializers import UserSerializer,UserProfileSerializer,SkillsSerializer,LearningSkillsSerializer,TeachingSkillsSerializer
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser

@api_view(['POST'])
def Signup(request):
    try:
        if request.method == 'POST':
            stream = io.BytesIO(request.body)
            parsed_data = JSONParser().parse(stream)
            serializer = UserSerializer(data = parsed_data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                      "message" : "Registered Successfully"
                    },
                    status=status.HTTP_201_CREATED,content_type='application/json')
            return Response(data=
                            {
                                "message" : serializer.errors
                            },status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return Response(data={
                        "message": "Method Not allowed"
                        }
                        ,status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as e:
        return Response({"message ": f"Unexpected Error occured {e}"},status= status.HTTP_500_INTERNAL_SERVER_ERROR, exception= True,content_type= "application/json")  

@api_view(['GET','PUT','PATCH'])
@permission_classes([IsAuthenticated])
def profile(request,id):
    try:
        userprofile = get_object_or_404(UserProfile,user__id=id)
        if request.method == 'GET':
            serializer = UserProfileSerializer(userprofile)
            return Response(serializer.data,status = status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(instance=userprofile,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                      "message" : "Updated Successfully"
                    },
                    status=status.HTTP_200_OK,content_type='application/json')
            return Response({"message" : serializer.errors},status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        elif request.method == 'PATCH':
            serializer = UserProfileSerializer(instance = userprofile,data = request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                      "message" : "Updated Successfully"
                    },
                    status=status.HTTP_200_OK,content_type='application/json')
            return Response({"message" : serializer.errors},status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        else:
            return Response(data={"message": "Method Not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as e:
        return Response({"message ": f"{str(e)}"},status= status.HTTP_404_NOT_FOUND, exception= True,content_type= "application/json")  

@api_view(['POST'])
@permission_classes(IsAdminUser)
def create_skills(request):
    try:
        serializer = SkillsSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "Skill created"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": f"Unexpected error occured {e}"},status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes(IsAuthenticated)
def fetch_skills(request):
    try:
        skills = Skills.objects.all()
        if request.method == 'GET':
            serializer = SkillsSerializer(skills)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"message": "No Skills found"},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT','PATCH','DELETE'])
@permission_classes(IsAdminUser)
def update_skills(request,id):
    try:
        skills = get_object_or_404(Skills,pk=id)
        if request.method == 'PUT':
            serializer = SkillsSerializer(instance=skills, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message" : "Skill updated successfully"},status = status.HTTP_200_OK)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        if request.method == 'PATCH':
            serializer = SkillsSerializer(instance = skills,data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message" : "Skill updated successfully"},status = status.HTTP_200_OK)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            deleted_data = SkillsSerializer(skills).data
            skills.delete()
            return Response({"message" : "Record deleted successfully","deleted_data" : deleted_data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": f"Unexpected error occured {str(e)}"},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@permission_classes(IsAuthenticated)
def create_teaching_skills(request):
    try:
        serializer = TeachingSkillsSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "Teaching Skill created"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": f"Unexpected error occured {str(e)}"},status= status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes(IsAuthenticated)
def fetch_teaching_skills(request):
    try:
        skills = TeachingSkills.objects.all()
        if request.method == 'GET':
            serializer = TeachingSkillsSerializer(skills)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"message": "No Skills found"},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": f"Unexpected error occured {str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes(IsAuthenticated)
def teaching_skills(request,id):
    try:
        teaching_skills = get_object_or_404(TeachingSkills,pk=id)
        if request.method == 'GET':
            seriaizer = TeachingSkillsSerializer(teaching_skills)
            return Response(seriaizer.data,status=status.HTTP_200_OK)
        if request.method == 'PUT':
            serializer = TeachingSkillsSerializer(instance=teaching_skills, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message" : "Skill updated successfully"},status = status.HTTP_200_OK)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        if request.method == 'PATCH':
            serializer = TeachingSkillsSerializer(instance = teaching_skills,data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message" : "Skill updated successfully"},status = status.HTTP_200_OK)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            deleted_data = TeachingSkillsSerializer(teaching_skills).data
            teaching_skills.delete()
            return Response({"message" : "Record deleted successfully","deleted_data" : deleted_data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@permission_classes(IsAuthenticated)
def create_learning_skills(request):
    try:
        serializer = LearningSkillsSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "Learning Skill created"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": f"Unexpected error occured {str(e)}"},status= status.HTTP_500_INTERNAL_SERVER_ERROR) 

@api_view(['GET'])
@permission_classes(IsAuthenticated)
def fetch_learning_skills(request):
    try:
        skills = LearningSkills.objects.all()
        if request.method == 'GET':
            serializer = LearningSkillsSerializer(skills)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"message": "No Skills found"},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": f"Unexpected error occured {str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes(IsAuthenticated)
def learning_skills(request,id):
    try:
        learning_skills = get_object_or_404(LearningSkills,pk=id)
        if request.method == 'GET':
            serializer = LearningSkillsSerializer(learning_skills)
            return Response(serializer.data,status = status.HTTP_200_OK)
        if request.method == 'PUT':
            serializer = LearningSkillsSerializer(instance=learning_skills, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message" : "Skill updated successfully"},status = status.HTTP_200_OK)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        if request.method == 'PATCH':
            serializer = LearningSkillsSerializer(instance = learning_skills,data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message" : "Skill updated successfully"},status = status.HTTP_200_OK)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            deleted_data = LearningSkillsSerializer(learning_skills).data
            learning_skills.delete()
            return Response({"message" : "Record deleted successfully","deleted_data" : deleted_data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)