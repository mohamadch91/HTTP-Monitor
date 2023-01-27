import jwt
from datetime import timedelta

from django.db.models.functions import datetime

from django.contrib.auth.models import User
from django.conf import settings
# generate jwt for user
def encode_user(user):
    username = user.username
    time_now = datetime.datetime.now()
    # create token
    
    jwt_token = jwt.encode({
        'username': username,
        "expire": str(time_now + timedelta(days=1)),
    },  
    key=settings.SECRET_KEY
    , algorithm='HS256')
    
    return jwt_token




def decode_jwt(token):
    try:
        decoded_token = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
        username=decoded_token['username']
        expire=decoded_token['expire']
        if expire < str(datetime.datetime.now()):
            return None
        else:
            if (User.objects.filter(username=username).exists()):
                return User.objects.get(username=username)
            else :
                return None
        
        
    except jwt.exceptions.DecodeError:
        return None