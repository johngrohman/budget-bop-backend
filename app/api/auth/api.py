from ninja import Router, Schema
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .schemas import UserSchema, LoginResponse, CreateUserSchema, LoginSchema
from .utils import create_access_token, create_refresh_token, validate_access_token, validate_refresh_token
from ninja.security import HttpBearer
from ninja.errors import HttpError

class ErrorSchema(Schema):
    detail: str

api = Router()

@api.get("/me", response=UserSchema)
def get_my_user(request):
    return request.auth

@api.post("/", response={200: LoginResponse, 409: ErrorSchema}, auth=None)
def create_user(request, payload: CreateUserSchema):

    username_unique = User.objects.filter(username=payload.username)

    if username_unique:
        raise HttpError(409, "Username already exists")

    user = User.objects.create_user(username=payload.username, password=payload.password)
    user.save()
    
    access_token = create_access_token({'user_id': user.id})

    print(f"User {user.username} created in successfully")

    return LoginResponse(
        access_token=access_token,
        token_type="Bearer",
        expires_in=900,
        user=UserSchema.from_orm(user)
    )


@api.post("/login", auth=None, response={200: LoginResponse, 401: ErrorSchema})
def login_view(request, payload: LoginSchema):
    user = authenticate(username=payload.username, password=payload.password)
    if user is None:
        print("Authentication failed")
        raise HttpError(401, "Invalid username or password")
    
    access_token = create_access_token({'user_id': user.id})
    refresh_token = create_refresh_token({'user_id': user.id})

    print(f"User {user.username} logged in successfully")
    response = JsonResponse({
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": 900,
        "user": 'test'
    })

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=7 * 24 * 3600,
        path="*",
    )

    return response

@api.post('/refresh', auth=None)
def refresh_access_token(request):
    crt = request.COOKIES.get('refresh_token')
    user_id = validate_refresh_token(crt)['user_id']

    
    new_access_token = create_access_token({'user_id': user_id})
    new_refresh_token = create_refresh_token({'user_id': user_id})

    response = JsonResponse({
        "access_token": new_access_token,
        "token_type": "Bearer",
        "expires_in": 900,
        "user": 'test'
    })

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=7 * 24 * 3600,
        path="*",
    )

    return response

@api.delete('/me')
def delete_acount(request):
    pass