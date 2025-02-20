from fastapi import HTTPException, status
from sqlalchemy import select, delete, and_, insert
from sqlalchemy.exc import IntegrityError
from controller.auth.schema.user import validate_user_data, MessageResponse, LogoutResponse, Token
from core.database.models import UsersTable, TokensTable
from core.database.base import async_session
from core.database.requests import TokenRequest, AuthRequest
from service.token.tokens import TokenService

class AuthService:
    @staticmethod
    async def register_user(username: str, email: str, password: str) -> MessageResponse:
        try:
            validated_user = validate_user_data(username=username, email=email, password=password)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

        async with async_session() as session:
            try:
                async with session.begin():
                    result = await session.execute(select(UsersTable).where(UsersTable.email == email))
                    existing_user = result.scalars().first()

                    if existing_user:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Пользователь с почтой {email} уже существует!"
                        )

                    hashed_password = await AuthRequest.hash_password(password)

                    stmt = (
                        insert(UsersTable)
                        .values(
                            username=validated_user.username,
                            email=validated_user.email,
                            password=hashed_password
                        )
                        .returning(UsersTable.id)
                    )
                    result = await session.execute(stmt)
                    user_id = result.scalar()

                tokens = await TokenService.generate_tokens(payload={
                    "user_id": user_id,
                    "username": validated_user.username,
                    "email": validated_user.email
                })

                refresh_token = tokens.get("refresh_token")
                if not refresh_token:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось создать refresh_token"
                    )

                await TokenRequest.save_token(user_id, refresh_token)
                return MessageResponse(message="Пользователь успешно зарегистрировался", user_id=user_id, token=Token(
                        refresh_token=refresh_token,
                        access_token=tokens.get("access_token")
                    ))

            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Ошибка при сохранении пользователя"
                )

    @staticmethod
    async def auth_user(username: str, email: str, password: str) -> MessageResponse:
        try:
            validate_user_data(username=username, email=email, password=password)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(UsersTable).where(and_(UsersTable.username == username, UsersTable.email == email))
                )
                user = result.scalar_one_or_none()

                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Пользователь с таким email не найден!"
                    )

                if not await AuthRequest.verify_password(password, user.password):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Неверный пароль!"
                    )

                # Генерация токенов
                tokens = await TokenService.generate_tokens(payload={
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email
                })

                refresh_token = tokens.get("refresh_token")
                if not refresh_token:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось создать refresh_token"
                    )

                try:
                    await TokenRequest.save_token(user_id=user.id, refresh_token=refresh_token)

                    return MessageResponse(message="Пользователь успешно авторизовался", user_id=user.id, token=Token(
                        refresh_token=refresh_token,
                        access_token=tokens.get("access_token")
                    ))

                except IntegrityError:
                    await session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Ошибка при сохранении токена"
                    )

    @staticmethod
    async def logout_user(refresh_token: str) -> LogoutResponse:
        async with async_session() as session:
            async with session.begin():
                await session.execute(delete(TokensTable).where(TokensTable.refresh_token == refresh_token))
        return LogoutResponse(message="Пользователь успешно вышел из системы")