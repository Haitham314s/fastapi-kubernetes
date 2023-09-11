from typing import List

from .hashing import get_password_hash
from .models import User
from .schema import UserIn


async def new_user_register(user: UserIn) -> User:
    password = get_password_hash(user.password)
    return await User.create(name=user.name, email=user.email, password=password)


async def get_all_users() -> List[User]:
    return await User.filter(email__not_isnull=True)


async def delete_user_service(user: User):
    user.description = f"Deleted user \nname: {user.name} \nemail: {user.email}"
    user.name = "Deleted user"
    user.email = None
    user.password = None

    await user.save()
