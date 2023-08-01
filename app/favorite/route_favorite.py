from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db, get_current_user
from ..auth.repository.user_repository import UserResponse
from .repository.favorite_repo import favorite_repo, FavoriteResponse
from ..announcement.repository.announcement_repository import announcement_repo

router = APIRouter(prefix="/auth/users/favorites/shanyraks", tags=["Favorites"])


@router.get("",response_model=List[FavoriteResponse])
async def get_favorites(current_user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    favorites = favorite_repo.get_all_favorites(current_user.id, db)
    if not favorites:
        return []
    return favorites or []

@router.post("/{announcement_id}")
async def add_to_favorite(announcement_id: int, current_user: UserResponse = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    if announcement_repo.get_announcement_by_id(db, announcement_id):
        favorite_repo.add_favorite(db, announcement_id, current_user.id)
        return {"message": "successful added"}
    raise HTTPException(status_code=404, detail="The announcement not found")


@router.delete("/{announcement_id}")
async def delete_at_announcement(favorite_id: int, current_user: UserResponse = Depends(get_current_user),
                                 db: Session = Depends(get_db)):
    get_favorite = favorite_repo.get_favorite_by_id(db, favorite_id)
    if get_favorite:
        if get_favorite.user_id == current_user.id:
            favorite_repo.delete_favorite(db, favorite_id)
            return {"message": "successful deleted"}
        raise HTTPException(status_code=403, detail="Forbidden: You are not authorized to delete this favorite")
    raise HTTPException(status_code=404, detail="The favorite not found")
