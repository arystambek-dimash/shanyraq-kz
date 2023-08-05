from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .repository.announcement_repository import announcement_repo, AnnouncementResponse, AnnouncementRequest
from ..dependencies import get_db, get_current_user
from ..auth.repository.user_repository import UserResponse
from ..comment.repository.comment_repo import comment_repo

router = APIRouter(prefix="/shanyraks", tags=["Announcements"])


@router.get("/all")
async def get_all_announcements(
        limit: int = Query(5, gt=0),
        offset: int = Query(1, ge=1),
        type: Optional[str] = Query(None, regex="^(sell|rent)$", examples=['sell', 'rent']),
        rooms_count: Optional[int] = Query(None, gt=0),
        price_from: Optional[float] = Query(None, ge=0),
        price_until: Optional[float] = Query(None, ge=0),
        db: Session = Depends(get_db)
):
    start = (offset - 1) * limit
    end = offset * limit
    announcements = announcement_repo.get_all(db)
    if type or rooms_count or price_from or price_until:
        filtered_announcements = [
            ad for ad in announcements
            if (not type or ad.type == type) and
               (not rooms_count or ad.rooms_count == rooms_count) and
               (not price_from or ad.price >= price_from) and
               (not price_until or ad.price <= price_until)
        ]
        total_announcements = len(filtered_announcements)
        return {
            "total": total_announcements,
            "announcements": [
                AnnouncementResponse(id=i.id, type=i.type, description=i.description, address=i.address, area=i.area,
                                     rooms_count=i.rooms_count, price=i.price, user_id=i.user_id,
                                     total_comments=i.total_comments, ) for i in filtered_announcements[start:end]]
        }
    return [AnnouncementResponse(id=i.id, type=i.type, description=i.description, address=i.address, area=i.area,
                                 rooms_count=i.rooms_count, price=i.price, user_id=i.user_id,
                                 total_comments=i.total_comments, ) for i in announcements[start:end]]


@router.post("/")
async def create_announcements(announcement: AnnouncementRequest,
                               current_user: UserResponse = Depends(get_current_user),
                               db: Session = Depends(get_db)):
    announcement.user_id = current_user.id
    return {"id": announcement_repo.create_announcement(db, announcement).id}


@router.get("/{id_announcement}", response_model=AnnouncementResponse)
async def get_announcement(id_announcement: int, db: Session = Depends(get_db)):
    announcement = announcement_repo.get_announcement_by_id(db, id_announcement)
    if not announcement:
        raise HTTPException(status_code=404, detail="The announcement not found")
    announcement.total_comments = comment_repo.get_length_comment(db, id_announcement)
    return announcement


@router.patch("/{id_announcement}")
async def update_announcement(id_announcement: int,
                              announcement: AnnouncementRequest,
                              current_user: UserResponse = Depends(get_current_user),
                              db: Session = Depends(get_db)):
    updating_announcement = announcement_repo.get_announcement_by_id(db, id_announcement)
    if not updating_announcement:
        raise HTTPException(status_code=404, detail="The announcement not found")
    if updating_announcement.user_id == current_user.id:
        announcement_repo.update_announcement(db, id_announcement, announcement)
        return {"message": "Successful updated"}
    raise HTTPException(status_code=403, detail="The user who placed the announcement")


@router.delete("/{id_announcement}")
async def delete_announcement(id_announcement: int,
                              current_user: UserResponse = Depends(get_current_user),
                              db: Session = Depends(get_db)):
    db_announcement = announcement_repo.get_announcement_by_id(db, id_announcement)
    if not db_announcement:
        raise HTTPException(status_code=404, detail="The announcement not found")
    if db_announcement.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="the user who placed the announcement")
    announcement_repo.delete_announcement(db, id_announcement)
    return {"message": "Successful Deleted"}
