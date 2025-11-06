from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
import json
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
import io
from .serializers import UserSerializer
from rest_framework import status

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
        return Response({"message ": "Unexpected Error occured {e}"},status= status.HTTP_500_INTERNAL_SERVER_ERROR, exception= True,content_type= "application/json")  
