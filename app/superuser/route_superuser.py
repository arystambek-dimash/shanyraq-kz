from fastapi import APIRouter, HTTPException, Depends
from ..dependencies import get_current_user, get_db
from ..auth.repository.user_repository import UserResponse, user_repo
from .repository.superuser_repo import superuser_repo

from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth/users/superuser", tags=["Superuser"])


@router.get("/get_users")
def get_all_users_only_super_user_can(current_user: UserResponse = Depends(get_current_user),
                                      db: Session = Depends(get_db)):
    if current_user.email == "dimash@gmail.com" or current_user.id in superuser_repo.get_all_superuser(db):
        return user_repo.get_all(db)
    raise HTTPException(status_code=400, detail="Ur are not superuser")


@router.get("/get_all_superuser")
def get_all_users_only_super_user_can(current_user: UserResponse = Depends(get_current_user),
                                      db: Session = Depends(get_db)):
    if current_user.email == "dimash@gmail.com" or current_user.id in superuser_repo.get_all_superuser(db):
        superusers = []
        for i in superuser_repo.get_all_superuser(db):
            superusers.append(user_repo.get_user_by_id(db,i.user_id))
        return superusers
    raise HTTPException(status_code=400, detail="Ur are not superuser")


@router.post("/appoint_as_admin")
def appoint_as_super_user(user_id: int, current_user: UserResponse = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    if (current_user.email == "dimash@gmail.com" or current_user.id in superuser_repo.get_all_superuser(
            db)) and user_repo.get_user_by_id(db, user_id) is not None:
        superuser_repo.make_superuser(db, current_user.id)
        return {"message": "The user was superuser"}
    raise HTTPException(status_code=400, detail="Ur are not superuser or the user not in database")


@router.delete("/delete_user")
def delete_user(user_id: int, current_user: UserResponse = Depends(get_current_user),
                db: Session = Depends(get_db)):
    if (current_user.email == "dimash@gmail.com" or current_user.id in superuser_repo.get_all_superuser(
            db)) and user_repo.get_user_by_id(db, user_id) is not None:
        user_repo.delete_user(db, user_id)
        return {"message": "The user was deleted"}
    raise HTTPException(status_code=400, detail="Ur are not superuser or the user not in database")
