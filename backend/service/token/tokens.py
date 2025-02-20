import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from typing import Optional, Dict, Any
from core.config import settings
from core.database.models import TokensTable, UsersTable
from core.database.base import async_session
from controller.auth.schema.user import UserModel
from core.database.requests import TokenRequest

private_key = settings.jwt_keys.get_private_key()
public_key = settings.jwt_keys.get_public_key()

class TokenService:
    @staticmethod
    async def validate_access_token(access_token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(access_token, public_key, algorithms=['RS256'])
            return payload
        except jwt.PyJWTError:
            return None

    @staticmethod
    async def validate_refresh_token(refresh_token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(refresh_token, public_key, algorithms=['RS256'])
            return payload
        except jwt.PyJWTError:
            return None

    @staticmethod
    async def generate_tokens(payload: Dict[str, Any]) -> Dict[str, str]:
        access_token = jwt.encode(
            {**payload, "exp": datetime.now(timezone.utc) + timedelta(days=20)},
            private_key,
            algorithm='RS256'
        )

        refresh_token = jwt.encode(
            {**payload, "exp": datetime.now(timezone.utc) + timedelta(days=14)},
            private_key,
            algorithm='RS256'
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    async def refresh_token(self, refresh_token: str):
        async with async_session() as session:
            async with session.begin():
                if not refresh_token:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Токена не существует!"
                    )

                token_data = await self.validate_refresh_token(refresh_token)
                if not token_data:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Неверный токен!"
                    )

                token_from_db = await session.execute(TokensTable).where(
                    TokensTable.refresh_token == refresh_token
                ).first()

                if not token_from_db:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Токен не найден в базе данных!"
                    )

                user = await session.execute(UsersTable).where(UsersTable.id == token_from_db.user_id).first()
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Пользователь не найден!"
                    )

                user_dto = UserModel(**user.to_dict())
                tokens = await self.generate_tokens(user_dto.model_dump())

                await TokenRequest.save_token(user_id=user_dto.id, refresh_token=tokens['refresh_token'])

                return tokens