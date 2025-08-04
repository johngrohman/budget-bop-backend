from ninja import Router, ModelSchema, Schema
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from ninja.security import HttpBearer
import secrets
import string

def generate_api_key(key_length=32):
    """
    Generate API keys with optional restrictions

    Args:
        key_length (int): Length of each API key
    """

    api_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(key_length))
    return ({ "key": api_key })


api = Router()

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class CreateUserSchema(Schema):
    username: str
    password: str


@api.get("/me", response=UserSchema)
def get_my_user(request):
    return request.auth

@api.post("/", response=UserSchema, auth=None)
def create_user(request, payload: CreateUserSchema):
    user = User.objects.create_user(username=payload.username, password=payload.password)
    user.save()
    login(request, user)
    return user


@api.post("/login", auth=None)
def login_view(request, payload: CreateUserSchema):
    user = authenticate(request, username=payload.username, password=payload.password)
    if user is None:
        print("Authentication failed")
        return JsonResponse({"success": False}, status=400)
    else:
        login(request, user)
        print(f"User {user.username} logged in successfully")
        return JsonResponse({"success": True})
    
@csrf_exempt
@api.post("/logout")
def logout_view(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        print(f"User {username} logged out successfully")
        return JsonResponse({"success": True})
    else:
        print("No authenticated user to log out")
        return JsonResponse({"success": False}, status=400)