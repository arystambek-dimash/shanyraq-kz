from fastapi import APIRouter, Depends, HTTPException
from .repository.user_repository import *
from ..dependencies import get_db, get_current_user, encode_to_jwt
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

router = APIRouter(
    prefix="",
)


@router.post("/auth/users/",tags=["Register"])
async def regis(user: UserRequest, db: Session = Depends(get_db)):
    existing_user = user_repo.get_user_by_email(db, user.email)
    if existing_user and (
            existing_user.email == user.email or
            existing_user.phone == user.phone
    ):
        raise HTTPException(status_code=400, detail="The phone number or email or username is already taken")
    user_repo.create_user(db, user)
    return {"message": "Successful Authorized"}


@router.post("/auth/users/login",tags=["Login"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = user_repo.get_user_by_email(db, form_data.username)
    if user is None:
        raise HTTPException(status_code=404, detail="The user not found")
    if user.password != form_data.password:
        raise HTTPException(status_code=404, detail="The password is inccorect")
    access_token = encode_to_jwt(user.id)
    return {"access_token": access_token}


@router.get("/auth/users/me/", response_model=UserResponse, tags=["Profile"])
async def profile(user: UserRequest = Depends(get_current_user)):
    return user


@router.patch("/auth/users/me/", tags=["Profile"])
async def profile_edit(user_update: UserUpdate,
                       user: UserRequest = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    if not user_repo.update_user(db, user.email, user_update):
        raise HTTPException(status_code=404,detail="Not found")
    user_repo.update_user(db, user.email, user_update)
    return {"messages": "successful updated"}
