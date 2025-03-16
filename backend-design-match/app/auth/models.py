from tortoise.models import Model
from tortoise import fields
from pydantic import BaseModel, EmailStr
from enum import Enum

# Role Enum
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

# Database User Model
class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=100, unique=True)
    username = fields.CharField(max_length=50)
    hashed_password = fields.CharField(max_length=128)
    role = fields.CharEnumField(UserRole, default=UserRole.USER)

# Pydantic Models for API
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    role: UserRole = UserRole.USER

class UserLogin(BaseModel):
    email: EmailStr
    password: str
