import strawberry
from pydantic import ValidationError
from fastapi import Response, Request
from controller.auth.schema.user import validate_user_data, LogoutResponse, MessageResponse
from service.users.auth import AuthService
from strawberry.types import Info

@strawberry.type
class AuthUser:
    @strawberry.mutation
    @staticmethod
    async def auth_user(username: str, password: str, email: str, info: Info) -> MessageResponse:
        response: Response = info.context['response']
        try:
            validate_user_data(username, email, password)
        except ValidationError as e:
            raise ValueError(f"Ошибка валидации: {e}")
        user_validate = await AuthService.auth_user(username=username, password=password, email=email)
        response.set_cookie(key="refresh_token", value=user_validate.token.refresh_token)
        return user_validate

@strawberry.type
class RegUser:
    @strawberry.mutation
    @staticmethod
    async def register_user(username: str, password: str, email: str, info: Info) -> MessageResponse:
        response: Response = info.context['response']
        try:
            validate_user_data(username, email, password)
        except ValidationError as e:
            raise ValueError(f"Ошибка валидации: {e}")
        user_validate = await AuthService.register_user(username=username, password=password, email=email)
        response.set_cookie(key="refresh_token", value=user_validate.token.refresh_token)
        return user_validate

@strawberry.type
class LogoutUser:
    @strawberry.mutation
    @staticmethod
    async def logout_user(info: Info) -> LogoutResponse:
        request: Request = info.context['request']
        refresh_token = request.cookies.get('refreshToken')
        user_logout = await AuthService.logout_user(refresh_token=refresh_token)
        return user_logout
        
@strawberry.type
class HelloWorld:
    @strawberry.field
    @staticmethod
    async def hello(name: str = "World") -> str:
        return f"Hello, {name}!"
