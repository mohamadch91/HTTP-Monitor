from authentications.jwt import decode_jwt

def get_user(request):
    token = request.headers.get('Authorization')
    if token:
        
        user=decode_jwt(token)
        if user:
            return user.pk
        else:
            return None
    else:
        return None