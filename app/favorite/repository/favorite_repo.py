from sqlalchemy.orm import Session
from sqlalchemy import delete
from pydantic import BaseModel
from ...database.models import Favorite, Announcement


class FavoriteResponse(BaseModel):
    shanyrak_id: int
    address: str


class FavoriteRepository:
    @staticmethod
    def get_all_favorites(user_id: int, db: Session):
        return db.query(Favorite).where(Favorite.user_id == user_id).all()

    @staticmethod
    def add_favorite(db: Session, announcement_id, user_id):
        get_announcement_by_id = db.query(Announcement).where(Announcement.id == announcement_id).first()
        favorite = Favorite(shanyrak_id=get_announcement_by_id.id, address=get_announcement_by_id.address, user_id=user_id)
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        return favorite

    @staticmethod
    def delete_favorite(db: Session, favorite_id):
        favorite = delete(Favorite).where(Favorite.id == favorite_id)
        db.execute(favorite)
        db.commit()
        return True

    @staticmethod
    def get_favorite_by_id(db: Session, favorite_id):
        return db.query(Favorite).filter(Favorite.id == favorite_id).first()


favorite_repo = FavoriteRepository()
