from datetime import timedelta

from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm

from database import db, select
from models.user import User
from schemas.user import User as Us
from utils.auth import create_access_token, admin_auth
from utils.environment import ACCESS_TOKEN_EXPIRE_MINUTES
from utils.exceptions import AccountDisabled, InvalidCredentials, NameDuplicated
from utils.crypt import hash_password, verify_password


router = APIRouter(tags=["/users"])


@router.post("/token")
async def login(data_form: OAuth2PasswordRequestForm = Depends()):
    if not (user := await User.get_user_by_name(data_form.username)) or not verify_password(user.password, data_form.password):
        return InvalidCredentials
    if not user.enabled:
        return AccountDisabled

    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    await user.create_session(access_token)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/new")
async def register(user: Us):
    if await User.get_user_by_name(user.name):
        return NameDuplicated

    user = await User.create(user.name, hash_password(user.password), user.enabled, user.admin)
    return user.serialize


@router.get("/users/all", dependencies=[admin_auth])
async def all_users(
    enabled: bool | None = Query(None),
    admin: bool | None = Query(None),
):
    query = select(User)
    if enabled is not None:
        query = query.where(User.enabled == enabled)
    if admin is not None:
        query = query.where(User.admin == admin)

    return {"users": [user.serialize async for user in await db.stream(query.order_by(User.id))]}
