from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from .models import UserProfile
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
import io
from .serializers import UserSerializer,UserProfileSerializer
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request,id):
    try:
        if request.method == 'GET':
            userprofile = get_object_or_404(UserProfile,user__id=id)
            serializer = UserProfileSerializer(userprofile)
            return Response(serializer.data,status = status.HTTP_200_OK)
        else:
            return Response(data={"message": "Method Not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as e:
        return Response({"message ": f"{str(e)}"},status= status.HTTP_404_NOT_FOUND, exception= True,content_type= "application/json")  

@api_view(['PUT','PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request,id):
    try:
        userprofile = get_object_or_404(UserProfile,id=id)
        if request.method == 'PUT':
            serializer = UserProfileSerializer(instance=userprofile,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                      "message" : "Updated Successfully"
                    },
                    status=status.HTTP_200_OK,content_type='application/json')
            return Response({"message" : serializer.errors},status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        if request.method == 'PATCH':
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
            return Response(data={ "message": "Method Not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as e:
        return Response({"message ": f"Unexpected Error occured {e}"},status= status.HTTP_500_INTERNAL_SERVER_ERROR, exception= True,content_type= "application/json")  
