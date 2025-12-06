from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,UserProfileSerializer,SkillsSerializer,LearningSkillsSerializer,TeachingSkillsSerializer
from .selectors import get_user_by_id,get_skill_object,get_teaching_skill_object,get_teaching_skill_by_id,get_learning_skill_by_id,get_learning_skill_object
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .services import get_ranked_users
import redis
import json
redis_client = redis.Redis(host="localhost",port=6379,decode_responses=True)

class Signup(APIView):

    def post(self,request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.save()
                message = {"message" : "User created successfully","user" : {"id": data.id,"username" : data.username}}
                return Response(message,status=status.HTTP_201_CREATED)
            return Response({"message" : serializer.errors},status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        except Exception as e:
            return Response({"message": f"Unexpected error occured {str(e)}"},status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class Profile(APIView):
    permission_classes= [IsAuthenticated]

    def get(self,request,id):
        try:
            serializer = UserProfileSerializer(get_user_by_id(id))
            if serializer.data:
                return Response(serializer.data,status = status.HTTP_200_OK)
            return Response({"message" : "No record found"},status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"Unexpected error occured {str(e)}"},status= status.HTTP_500_INTERNAL_SERVER_ERROR)
       
    def put(self,request,id):
        try:
            serializer = UserProfileSerializer(instance= get_user_by_id(id),data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message" : "Updated Successfully"},status=status.HTTP_200_OK,content_type='application/json')
            return Response({"message" : serializer.errors},status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        except Exception as e:
            return Response({"message": f"Unexpected error occured {str(e)}"},status= status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self,request,id):
        try:
            serializer = UserProfileSerializer(instance = get_user_by_id(id),data = request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message" : "Updated Successfully"},status=status.HTTP_200_OK,content_type='application/json')
            return Response({"message" : serializer.errors},status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        except Exception as e:
            return Response({"message": f"Unexpected error occured {str(e)}"},status= status.HTTP_500_INTERNAL_SERVER_ERROR)          

class Skill(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            serializer = SkillsSerializer(instance = get_skill_object(),many = True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"Unexpected error occured {str(e)}"},status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class TeachSkill(APIView):
    permission_classes= [IsAuthenticated]

    def post(self,request):
        try:
            serializer = TeachingSkillsSerializer(data = request.data)
            if serializer.is_valid():
                data =serializer.save()
                return Response({"message" : "Teaching Skill created","teach-skill": data.id },status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"Unexpected error occured {str(e)}"},status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self,request,id=None):
        try:
            if id:
                serializer = TeachingSkillsSerializer(get_teaching_skill_by_id(id))
            else:
                serializer = TeachingSkillsSerializer(get_teaching_skill_object(), many= True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"Unexpected error occured {str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self,request,id):
        try:
            serializer = TeachingSkillsSerializer(instance=get_teaching_skill_by_id(id), data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message" : "Teaching Skill updated successfully"},status = status.HTTP_200_OK)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"Unexpected error occured {str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self,request,id):
        try:
            serializer = TeachingSkillsSerializer(instance=get_teaching_skill_by_id(id), data = request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message" : "Teaching Skill updated successfully"},status = status.HTTP_200_OK)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"Unexpected error occured {str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request,id):
        try:
            teaching_skill = get_teaching_skill_by_id(id)
            if teaching_skill:
                teaching_skill.delete()
                return Response({"message": "Record deleted successfully"},status=status.HTTP_200_OK)
            return Response({"message": "Record not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": f"Unexpected error occured {str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LearnSkill(APIView):
    permission_classes= [IsAuthenticated]

    def post(self,request):
        try:
            serializer = LearningSkillsSerializer(data = request.data)
            if serializer.is_valid():
                data =serializer.save()
                return Response({"message" : "Learning Skill created","learn-skill": data.id },status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"Unexpected error occured {str(e)}"},status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self,request,id=None):
        try:
            if id:
                serializer = LearningSkillsSerializer((get_learning_skill_by_id(id)))
            else:
                serializer = LearningSkillsSerializer(get_learning_skill_object(), many= True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"Unexpected error occured {str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self,request,id):
        try:
            serializer = LearningSkillsSerializer(instance=get_learning_skill_by_id(id), data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message" : "Learning Skill updated successfully"},status = status.HTTP_200_OK)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"Unexpected error occured {str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self,request,id):
        try:
            serializer = LearningSkillsSerializer(instance=get_learning_skill_by_id(id), data = request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message" : "Learning Skill updated successfully"},status = status.HTTP_200_OK)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"Unexpected error occured {str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request,id):
        try:
            teaching_skill = get_learning_skill_by_id(id)
            if teaching_skill:
                teaching_skill.delete()
                return Response({"message": "Record deleted successfully"},status=status.HTTP_200_OK)
            return Response({"message": "Record not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": f"Unexpected error occured {str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    try:
        user = request.user
        cache_key = user.id
        cached = redis_client.get(cache_key)
        if cached:
            data = json.loads(cached) 
            return Response(data=data,status=status.HTTP_200_OK)
        users = get_ranked_users(user)
        data={
            "matches": [{
                    "id": u["user"].id,
                    "profile_id" : u["user"].profile.id if u["user"].profile else None,
                    "username": u["user"].username,
                    "skills" : [u.skill.name for u in u["user"].teaching_skill.all()],
                    "area_of_interest" : u["user"].profile.interest if u["user"].profile else None,
                    "bio" : u["user"].profile.bio if u["user"].profile else None,
                    "learning_skills" : [u.skills.name for u in u["user"].learning_skill.all()]
                }
                for u in users ]}
        redis_client.set(cache_key,json.dumps(data),ex=300)
        return Response(data=data,status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message" : str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)