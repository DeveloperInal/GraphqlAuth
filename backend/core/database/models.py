from datetime import datetime
from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import event
from core.database.base import Base

class UsersTable(Base):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    tokens: Mapped[list["TokensTable"]] = relationship("TokensTable", back_populates="user")

class TokensTable(Base):
    __tablename__ = 'tokens'

    refresh_token: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    user: Mapped["UsersTable"] = relationship("UsersTable", back_populates="tokens")

# Автоматическое обновление updated_at
@event.listens_for(UsersTable, 'before_update')
def update_updated_at(mapper, connection, target):
    target.updated_at = datetime.now()