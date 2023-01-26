
# import the necessary packages


from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from .jwt import encode_user
class RegisterView(APIView):
    # register user
    def post(self,request)-> Response:
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
    
    # login user
    def post(self,request)-> Response:
        
        if not request.data['username'] or not request.data['password']:
            return Response({"message":"Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        username=request.data['username']
        password=request.data['password']        
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"message":"Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        token = encode_user(user)
        return Response({"access":token}, status=status.HTTP_200_OK)
        
    

