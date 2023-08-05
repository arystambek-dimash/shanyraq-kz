from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String(32), unique=True, index=True)
    password = Column(String(32))
    name = Column(String(30))
    city = Column(String(15))

    announcements = relationship('Announcement', back_populates='users', cascade="all,delete")
    comments = relationship('Comment', back_populates='users')
    favorites = relationship('Favorite', back_populates='user', cascade="all,delete")


class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    price = Column(Float)
    address = Column(String)
    area = Column(Float)
    rooms_count = Column(Integer)
    description = Column(String)

    total_comments = Column(Integer)

    user_id = Column(ForeignKey('users.id', ondelete="CASCADE"))

    comments = relationship('Comment', back_populates='announcements', cascade="all,delete")
    users = relationship('User', back_populates='announcements', cascade="all,delete")
    favorites = relationship('Favorite', back_populates='announcement', cascade="all,delete")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    announcement_id = Column(Integer, ForeignKey("announcements.id", ondelete="CASCADE"))

    created_at = Column(TIMESTAMP, default=datetime.now().replace(second=0, microsecond=0))

    announcements = relationship('Announcement', back_populates='comments', cascade="all,delete")
    users = relationship('User', back_populates='comments')


class SuperUser(Base):
    __tablename__ = "superusers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey('users.id'))


class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True, index=True)
    shanyrak_id = Column(ForeignKey('announcements.id', ondelete="CASCADE"))  # Updated here
    address = Column(String)
    user_id = Column(ForeignKey('users.id', ondelete="CASCADE"))

    announcement = relationship('Announcement', back_populates='favorites', cascade="all,delete")  # Updated here
    user = relationship('User', back_populates='favorites', cascade="all,delete")
