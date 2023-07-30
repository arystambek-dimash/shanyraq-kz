from fastapi import APIRouter
from ..dependencies import *
from ..announcement.repository.announcement_repository import announcement_repo
from ..auth.repository.user_repository import UserResponse
from .repository.comment_repo import CommentRequest, comment_repo

router = APIRouter(prefix="/shanyraks/{id_announcement}", tags=["Comments"])


@router.get("/comments")
async def get_comment(id_announcement: int,
                      db: Session = Depends(get_db)):
    if id_announcement and announcement_repo.get_announcement_by_id(db, id_announcement):
        return comment_repo.get_comment_by_announcement_id(db, id_announcement)
    raise HTTPException(status_code=404, detail="The announcement not found")


@router.post("/comments")
async def create_comment(id_announcement: int, comment: CommentRequest,
                         current_user: UserResponse = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    if id_announcement and announcement_repo.get_announcement_by_id(db, id_announcement):
        comment_repo.create_comment(db, current_user.id, id_announcement, comment)
        return {"message": "Comment was public"}
    raise HTTPException(status_code=404, detail="The announcement not found")


@router.patch("/comments/{comment_id}")
async def update_comment(id_announcement: int, comment_id: int, comment: CommentRequest,
                         current_user: UserResponse = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    if not announcement_repo.get_announcement_by_id(db,id_announcement):
        raise HTTPException(status_code=404,detail="The announcement not found")
    db_comment = comment_repo.get_comment_by_announcement_id_with_comment_id(db, id_announcement, comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="The comment not found or Ur not user which created the comment")
    if db_comment.user_id == current_user.id and db_comment:
        comment_repo.update_comment(db, announcement_id=id_announcement, user_id=current_user.id, comment_id=comment_id,
                                    comment=comment)
        return {"message": "Comment was successful updated"}
    raise HTTPException(status_code=404, detail="The comment not found or Ur not user which created the comment")


@router.delete("/comments/{comment_id}")
async def delete_comment(id_announcement: int, comment_id: int,
                         current_user: UserResponse = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    if not announcement_repo.get_announcement_by_id(db,id_announcement):
        raise HTTPException(status_code=404,detail="The announcement not found")
    db_comment = comment_repo.get_comment_by_announcement_id_with_comment_id(db, id_announcement, comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="The comment not found")
    if db_comment.user_id == current_user.id or current_user.is_superuser:
        comment_repo.delete_comment(db, announcement_id=id_announcement, user_id=current_user.id, comment_id=comment_id)
        return {"message": "Comment was successful deleted"}
    raise HTTPException(status_code=404, detail="The comment not found or ur not the creater")
