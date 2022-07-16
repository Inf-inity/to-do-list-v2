from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, SmallInteger, String
from sqlalchemy.orm import Mapped, relationship

from database import Base, db
from utils.logger import get_logger

from .user import User


logger = get_logger(__name__)


class UserTask(Base):
    __tablename__ = "user_tasks"

    id: Mapped[int] = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    creator: User = relationship("User", back_populates="tasks")
    creator_id: Mapped[int] = Column(BigInteger, ForeignKey("users.id"))
    title: Mapped[str] = Column(String(64))
    description: Mapped[str] = Column(String(4096))
    timestamp: Mapped[datetime] = Column(DateTime)
    end: Mapped[datetime] = Column(DateTime, nullable=True, default=None)
    resolved: Mapped[bool] = Column(Boolean, default=False)
    priority: Mapped[int] = Column(SmallInteger, default=1)

    @staticmethod
    async def create(title: str, description: str, end: datetime, prio: int, creator: User) -> UserTask:
        task = UserTask(
            title=title, description=description, timestamp=datetime.utcnow(), end=end, priority=prio, creator_id=creator.id,
        )
        await db.add(task)
        logger.debug(f"Task '{title}' was created")

        return task

    async def remove(self):
        await db.delete(self)
        logger.debug(f"Task '{self.title}' was deleted!")

    @property
    def serialize(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "created_at": self.timestamp.timestamp(),
            "ends_at": self.end.timestamp(),
            "resolved": self.resolved,
            "creator": self.creator_id
        }

    @staticmethod
    async def get_by_id(task_id: int) -> UserTask | None:
        return await db.get(UserTask, id=task_id)
