from ninja import Schema, ModelSchema
from typing import Optional
from django.contrib.auth.models import User

class UserSchema(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str

    class Config:
        orm_mode: True

class CreateUserSchema(Schema):
    username: str
    password: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class LoginSchema(Schema):
    username: str
    password: str

class LoginResponse(Schema):
    access_token: str
    token_type: str
    expires_in: int
    user: UserSchema