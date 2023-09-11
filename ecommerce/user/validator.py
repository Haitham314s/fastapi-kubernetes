from typing import Optional

from .models import User


async def verify_email_exist(email: str) -> Optional[User]:
    return await User.get_or_none(email=email)
