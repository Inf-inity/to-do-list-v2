from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

from models.user import User
from schemas.token import Token
from schemas.user import User as Us
from utils.auth import create_access_token, get_current_user
from utils.environment import ACCESS_TOKEN_EXPIRE_MINUTES
from utils.crypt import hash_password, verify_password


router = APIRouter(tags=["/auth"])


@router.post("/login", response_model=Token)
async def login(data_form: OAuth2PasswordRequestForm = Depends()):
    if not (user := await User.get_user_by_name(data_form.username)):
        return HTTPException(status_code=400, detail="Invalid password or username")
    if not verify_password(user.password, data_form.password):
        return HTTPException(status_code=400, detail="Invalid password or username")
    if not user.enabled:
        return HTTPException(status_code=400, detail="Account is disabled")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True, expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return response


@router.post("/register")
async def register(user: Us):
    if await User.get_user_by_name(user.name):
        return "User already with this name"

    return await User.create(user.name, hash_password(user.password), True, False)


@router.get("/logout")
async def logout(_: Us = Depends(get_current_user)):
    response = RedirectResponse("/login", status_code=200)
    response.delete_cookie("access_token")

    return response
