from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .repository.announcement_repository import announcement_repo, AnnouncementResponse, AnnouncementRequest
from ..dependencies import get_db, get_current_user
from ..auth.repository.user_repository import UserResponse
from ..comment.repository.comment_repo import comment_repo

router = APIRouter(prefix="",tags=["Announcements"])


@router.get("/shanyraks/all")
async def get_all_announcements(db: Session = Depends(get_db)):
    announcements = announcement_repo.get_all(db)
    for i in announcements:
        if comment_repo.get_comment_by_announcement_id(db, i.id):
            i.total_comments = comment_repo.get_length_comment(db, i.id)
    return announcements


@router.post("/shanyraks/")
async def create_announcements(announcement: AnnouncementRequest,
                               current_user: UserResponse = Depends(get_current_user),
                               db: Session = Depends(get_db)):
    announcement.user_id = current_user.id
    return {"id": announcement_repo.create_announcement(db, announcement).id}


@router.get("/shanyraks/{id_announcement}", response_model=AnnouncementResponse)
async def get_announcement(id_announcement: int, db: Session = Depends(get_db)):
    announcement = announcement_repo.get_announcement_by_id(db, id_announcement)
    if not announcement:
        raise HTTPException(status_code=404, detail="The announcement not found")
    announcement.total_comments = comment_repo.get_length_comment(db, id_announcement)
    return announcement


@router.patch("/shanyraks/{id_announcement}")
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
    raise HTTPException(status_code=404, detail="The flower ID is incorrect or you are not"
                                                "the user who placed the announcement")


@router.delete("/shanyraks/{id_announcement}")
async def delete_announcement(id_announcement: int,
                              current_user: UserResponse = Depends(get_current_user),
                              db: Session = Depends(get_db)):
    db_announcement = announcement_repo.get_announcement_by_id(db, id_announcement)
    if not db_announcement:
        raise HTTPException(status_code=404, detail="The announcement not found")
    if db_announcement.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="The flower ID is incorrect or you are not"
                                                    "the user who placed the announcement")
    announcement_repo.delete_announcement(db, id_announcement)
    return {"message": "Successful Deleted"}
