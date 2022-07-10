from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Column, DateTime, String
from sqlalchemy.orm import Mapped

from database import Base, db, select
from utils.crypt import hash_password
from utils.environment import ADMIN_USERNAME, ADMIN_PASSWORD
from utils.logger import get_logger


logger = get_logger(__name__)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    name: Mapped[str] = Column(String(32), unique=True)
    password: Mapped[str | None] = Column(String(512), nullable=True)
    registration: Mapped[datetime] = Column(DateTime)
    enabled: Mapped[bool] = Column(Boolean, default=True)
    admin: Mapped[bool] = Column(Boolean, default=False)

    @staticmethod
    async def create(name: str, password: str | None = None, enabled: bool = True, admin: bool = False) -> User:
        user = User(
            name=name, password=password, registration=datetime.utcnow(), enabled=enabled, admin=admin
        )
        await db.add(user)
        logger.debug(f"User {name} was added!")
        return user

    @staticmethod
    async def init_admin() -> User | None:
        if await db.exists(select(User)):
            return

        user = await User.create(name=ADMIN_USERNAME, password=hash_password(ADMIN_PASSWORD), enabled=True, admin=True)
        logger.info(f"Admin user '{ADMIN_USERNAME}' has been created!")
        return user

    async def remove(self):
        await db.delete(self)
        logger.debug(f"User {self.name} was deleted!")

    @staticmethod
    async def get_user_by_name(name: str) -> User | None:
        return await db.get(User, name=name)
