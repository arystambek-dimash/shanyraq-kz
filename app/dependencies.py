from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database.database import SessionLocal
from jose import jwt


from .auth.repository.user_repository import user_repo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/users/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def encode_to_jwt(user_id):
    body = {"user_id": user_id}
    return jwt.encode(body, "shanyraq", algorithm="HS256")


def decode_access_token(token):
    data = jwt.decode(token, "shanyraq", algorithms=["HS256"])
    return data["user_id"]


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = user_repo.get_user_by_id(db, int(decode_access_token(token)))
    if not user:
        raise HTTPException(status_code=404, detail="Not user such username")
    return user