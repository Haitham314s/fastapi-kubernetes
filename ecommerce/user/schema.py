from uuid import UUID

from pydantic import BaseModel, EmailStr, constr
from tortoise.contrib.pydantic import pydantic_model_creator

from ecommerce.user.models import User

UserGenOut = pydantic_model_creator(User, include={"id", "name", "email"})


class UserIn(BaseModel):
    name: constr(min_length=2, max_length=50)
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: UUID
    name: str
    email: str
