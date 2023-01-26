from rest_framework.response import Response
from authentications.jwt import decode_jwt
from rest_framework import status


def get_user(request):
    token = request.headers.get('Authorization')
    if token:
        
        user=decode_jwt(token)
        if user:
            return user.id
        else:
            return Response({"message":"You are not authorized to view this endpoint"}, status=status.HTTP_401_UNAUTHORIZED)        
        
    return Response({"message":"You are not authorized to view this endpoint"}, status=status.HTTP_401_UNAUTHORIZED)