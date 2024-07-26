
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: int | None = Field(default=None)
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str



