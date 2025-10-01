
import threading
from django.utils.deprecation import MiddlewareMixin
from app.api.auth.utils import validate_access_token
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from jwt import ExpiredSignatureError, InvalidTokenError

User = get_user_model()

_user_storage = threading.local()

def set_current_user(user):
    _user_storage.user = user

def get_current_user():
    return getattr(_user_storage, 'user', None)

class CurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        Attach user to request object
        """
        try:
            auth_header = request.COOKIES['access_token']
        except KeyError:
            request.user = AnonymousUser
            return

        # If there's no authorizaiton header or if it's not Bearer
        if not auth_header:
            request.user = AnonymousUser()
            return
        
        # Validate token and set the requests user
        try:
            payload = validate_access_token(auth_header)
            user_id = payload.get("user_id")

            if not user_id:
                request.user = AnonymousUser()
                return

            try:
                user = User.objects.get(pk=user_id)
                request.user = user
                set_current_user(user)
                print('request.user', user.id)
            except User.DoesNotExist:
                request.user = AnonymousUser()

        except (ExpiredSignatureError, InvalidTokenError):
            request.user = AnonymousUser()
