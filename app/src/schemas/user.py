from pydantic import BaseModel


class User(BaseModel):
    name: str
    password: str
    enabled: bool
    admin: bool
