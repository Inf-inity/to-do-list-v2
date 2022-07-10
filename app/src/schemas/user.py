from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    id: int = None
    name: str
    password: str
    registration: datetime = None
    enabled: bool = True
    admin: bool = False
