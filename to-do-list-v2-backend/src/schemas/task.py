from datetime import datetime
from pydantic import BaseModel


class Task(BaseModel):
    title: str = ""
    description: str = ""
    end: datetime | None = None
    priority: int = 1
