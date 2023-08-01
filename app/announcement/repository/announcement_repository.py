from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import update, delete
from ...database.models import Announcement


class AnnouncementRequest(BaseModel):
    type: str
    price: float
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: int = None

    class Config:
        json_schema_extra = {
            "example": {
                "type": "rent",
                "price": 15000,
                "address": "Astana,Almaty r-n",
                "area": 46.5,
                "rooms_count": 2,
                "description": "Here description"
            }
        }


class AnnouncementResponse(BaseModel):
    id: int
    type: str
    price: float
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: int
    total_comments: int


class AnnouncementRepository:
    @staticmethod
    def get_announcement_by_id(db: Session, announcement_id):
        return db.query(Announcement).filter(Announcement.id == announcement_id).first()

    @staticmethod
    def create_announcement(db: Session, announcement: AnnouncementRequest):
        db_announcement = Announcement(type=announcement.type, price=announcement.price,
                                       address=announcement.address, area=announcement.area,
                                       rooms_count=announcement.rooms_count,
                                       description=announcement.description,
                                       total_comments=0,
                                       user_id=announcement.user_id)

        db.add(db_announcement)
        db.commit()
        db.refresh(db_announcement)
        return db_announcement

    @staticmethod
    def update_announcement(db: Session, announcement_id, announcement: AnnouncementRequest):
        update_announcement = update(Announcement).where(Announcement.id == announcement_id).values(
            type=announcement.type, price=announcement.price,
            address=announcement.address, area=announcement.area,
            rooms_count=announcement.rooms_count,
            description=announcement.description,
        )

        db.execute(update_announcement)
        db.commit()
        updated_announcement = db.query(Announcement).get(announcement_id)
        if updated_announcement:
            return updated_announcement
        raise HTTPException(status_code=404, detail="Not found such announcement id")

    @staticmethod
    def delete_announcement(db: Session, announcement_id):
        delete_announcement = delete(Announcement).where(Announcement.id == announcement_id)

        db.execute(delete_announcement)
        db.commit()

    @staticmethod
    def get_all(db: Session):
        return db.query(Announcement).all()


announcement_repo = AnnouncementRepository()
