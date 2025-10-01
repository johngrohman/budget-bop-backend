from datetime import timedelta, datetime
import jwt
from ninja.security import HttpBearer, APIKeyCookie
from ninja.errors import HttpError
from django.contrib.auth.models import User

# Key used to sign
ACCESS_TOKEN_KEY = 'test-access'
REFRESH_TOKEN_KEY = 'test-refresh'
ALGORITHM = 'HS256'

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expires = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expires})
    return jwt.encode(to_encode, ACCESS_TOKEN_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)):
    to_encode = data.copy()
    expires = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expires})
    return jwt.encode(to_encode, REFRESH_TOKEN_KEY, algorithm=ALGORITHM)

def validate_access_token(token: str):
    payload = jwt.decode(token, ACCESS_TOKEN_KEY, algorithms=[ALGORITHM])
    return payload

def validate_refresh_token(token: str):
    try:
        payload = jwt.decode(token, REFRESH_TOKEN_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HttpError(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HttpError(401, "Invalid token")
    except:
        return None

class JWTAuthCookie(APIKeyCookie):
    def authenticate(self, request, key):
        try:
            token = request.COOKIES['access_token']
            payload = validate_access_token(token)
            user_id = payload.get('user_id')
        except jwt.ExpiredSignatureError:
            raise HttpError(401, "Token expired")
        except jwt.InvalidTokenError:
            raise HttpError(401, "Invalid token")
        except:
            return None
            
        if not user_id:
            raise HttpError(401, "Invalid token payload")
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise HttpError(401, "User not found")
        
        return user