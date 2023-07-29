from sqlalchemy.orm import Session
from ...database.models import SuperUser


class SuperUserRepository:
    @staticmethod
    def make_superuser(db: Session, user_id):
        superuser = SuperUser(user_id=user_id)
        db.add(superuser)
        db.commit()
        db.refresh(superuser)
        return superuser

    @staticmethod
    def get_all_superuser(db: Session):
        return db.query(SuperUser).all()


superuser_repo = SuperUserRepository()
