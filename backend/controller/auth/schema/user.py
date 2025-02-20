<<<<<<< HEAD
import strawberry
from pydantic import BaseModel, EmailStr, ValidationError

class UserModel(BaseModel):
    username: str
    email: EmailStr
    password: str

@strawberry.type
class User:
    username: str
    email: str
    password: str

@strawberry.type
class LogoutResponse:
    message: str

@strawberry.type
class Token:
    access_token: str
    refresh_token: str

@strawberry.type
class MessageResponse:
    message: str
    user_id: str
    token: Token

def validate_user_data(username: str, email: str, password: str) -> UserModel:
    try:
        user_model = UserModel(
            username=username,
            email=email, # type: ignore
            password=password)
        return user_model
    except ValidationError as e:
=======
import strawberry
from pydantic import BaseModel, EmailStr, ValidationError

class UserModel(BaseModel):
    username: str
    email: EmailStr
    password: str

@strawberry.type
class User:
    username: str
    email: str
    password: str

@strawberry.type
class LogoutResponse:
    message: str

@strawberry.type
class Token:
    access_token: str
    refresh_token: str

@strawberry.type
class MessageResponse:
    message: str
    user_id: str
    token: Token

def validate_user_data(username: str, email: str, password: str) -> UserModel:
    try:
        user_model = UserModel(
            username=username,
            email=email, # type: ignore
            password=password)
        return user_model
    except ValidationError as e:
>>>>>>> d8a3317a0a70d13af2213931a89ea36727542756
        raise ValueError(f"Ошибка валидации: {e}")