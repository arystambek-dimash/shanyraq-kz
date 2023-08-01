from ...database.models import User
from pydantic import BaseModel, EmailStr, Field,ValidationError, validator
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlalchemy.orm import Session
from sqlalchemy import update, delete


class UserRequest(BaseModel):
    email: EmailStr
    phone: PhoneNumber = Field(max_length=32, min_length=10)
    password: str = Field(max_length=32, min_length=8)
    name: str = Field(max_length=30)
    city: str = Field(max_length=15)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "nfactorial@school.com",
                "phone": "+77775551122",
                "password": "password123",
                "name": "Dalida",
                "city": "Almaty"
            },
        }


class UserResponse(BaseModel):
    id: int
    email: str
    phone: str
    name: str
    city: str


class UserUpdate(BaseModel):
    phone: PhoneNumber
    name: str
    city: str


class UserRepostitory:
    @staticmethod
    def get_user_by_email(db: Session, email):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create_user(db: Session, user: UserRequest):
        db_user = User(email=user.email, phone=user.phone[4:], password=user.password,
                       name=user.name, city=user.city)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def update_user(db: Session, user_email, user: UserUpdate):
        db_update = update(User).where(User.email == user_email).values(phone=user.phone[4:],
                                                                        name=user.name,
                                                                        city=user.city,
                                                                        )
        db.execute(db_update)
        db.commit()
        updated_user = db.query(User).get(user_email)
        return updated_user

    @staticmethod
    def get_all(db: Session):
        return db.query(User).all()

    @staticmethod
    def delete_user(db: Session, user_id):
        db.execute(delete(User).where(User.id == user_id))
        db.commit()


user_repo = UserRepostitory()
