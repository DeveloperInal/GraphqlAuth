<<<<<<< HEAD
import uuid

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import String
from core.config import settings

engine = create_async_engine(url=settings.url_database, echo=False)
async_session = async_sessionmaker(bind=engine, expire_on_commit=True)

def generate_cuid():
    return str(uuid.uuid4())

class Base(DeclarativeBase, AsyncAttrs):
=======
import uuid

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import String
from core.config import settings

engine = create_async_engine(url=settings.url_database, echo=False)
async_session = async_sessionmaker(bind=engine, expire_on_commit=True)

def generate_cuid():
    return str(uuid.uuid4())

class Base(DeclarativeBase, AsyncAttrs):
>>>>>>> d8a3317a0a70d13af2213931a89ea36727542756
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_cuid)