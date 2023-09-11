from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ecommerce.user import User
from ecommerce.user.hashing import verify_password

from .jwt import create_access_token

router = APIRouter(tags=["Auth"])


@router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(email=request.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password"
        )

    # Generate a JWT token
    access_token = create_access_token(data={"user_id": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
