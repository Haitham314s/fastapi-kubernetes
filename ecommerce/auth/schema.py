from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_tye: str


class TokenData(BaseModel):
    id: Optional[UUID] = None
