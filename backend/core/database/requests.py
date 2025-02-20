import bcrypt
from core.database.base import async_session
from core.database.models import TokensTable
from sqlalchemy import select, delete

class AuthRequest:
    @staticmethod
    async def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    async def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

class TokenRequest:
    @staticmethod
    async def save_token(user_id: str, refresh_token: str):
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(TokensTable).filter(TokensTable.user_id == user_id))
                existing_token = result.scalars().first()

                if existing_token:
                    existing_token.refresh_token = refresh_token
                else:
                    new_token = TokensTable(user_id=user_id, refresh_token=refresh_token)
                    session.add(new_token)

    @staticmethod
    async def remove_token(refresh_token: str):
        async with async_session() as session:
            async with session.begin():
                refresh_token = await session.execute(delete(TokensTable).where(TokensTable.refresh_token == refresh_token))
                return refresh_token