import jwt
import datetime
from django.contrib.auth.models import User
from django.conf import settings
# generate jwt for user
def encode_user(user):
    username = user.username
    time_now = datetime.datetime.now()
    # create token
    
    jwt_token = jwt.encode({
        'username': username,
        "expire": time_now + datetime.timedelta(days=1),
    },  
    key=settings.SECRET_KEY
    , algorithm='HS256')
    
    return jwt_token








def decode_kwt(token):
    try:
        decoded_token = jwt.decode(token, verify=False)
        
    except jwt.exceptions.DecodeError:
        return None