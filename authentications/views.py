
# import the necessary packages


from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt
import datetime

class RegisterView(APIView):
    # register user
    def post(self,request):
        if not request.data['username'] or not request.data['password']:
            return Response({"message":"Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
            
        username=request.data['username']
        password=request.data['password']
        if User.objects.filter(username=username).exists():
            return Response({"message":"User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        # create user
        User.objects.create_user(username=username,password=password)
        return Response({"message":"User created successfully"}, status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    pass
        
        

    

