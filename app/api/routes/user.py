from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import CurrentUser, DbConnection
from app.core.db import user_table
from app.core.security import create_access_token, hash_password, verify_password
from app.crud import find_user_by_email
from app.models import Message, RegistrationResponse, Token, User, UserIn

router = APIRouter()


@router.get("/welcome")
async def greeting() -> Message:
    return Message(message="Hello, welcome to the User API!")


@router.post("/user", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserIn, db_conn: DbConnection) -> RegistrationResponse:
    user = await find_user_by_email(db_conn, user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists, please use another email",
        )
    try:
        stmt = user_table.insert().values(
            username=user_in.username,
            email=user_in.email,
            password_hash=hash_password(user_in.password.get_secret_value()),
        )
        result = await db_conn.execute(stmt)
        await db_conn.commit()
    except Exception:
        await db_conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, please try again",
        ) from None
    return RegistrationResponse(
        success=True,
        message="Registration successful",
        id=result.inserted_primary_key[0],
    )


@router.post("/token", response_model=Token)
async def login_access_token(
    db_conn: DbConnection,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await find_user_by_email(db_conn, form_data.username)
    if user is None or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    token = create_access_token(user.uid)
    return Token(access_token=token)


@router.get("/users/me", response_model=User)
async def get_logged_in_user_profile(current_user: CurrentUser) -> User:
    return User.model_validate(current_user)


@router.delete("/users/me", response_model=Message)
async def delete_logged_in_user(current_user: CurrentUser, db_conn: DbConnection) -> Message:
    try:
        stmt = user_table.delete().where(user_table.c.uid == current_user.uid)
        await db_conn.execute(stmt)
        await db_conn.commit()
    except Exception:
        await db_conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting your account",
        ) from None
    return Message(message="User deleted successfully")
