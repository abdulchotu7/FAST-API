from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    bookings = relationship("Booking", back_populates="user")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    showtime = Column(DateTime)
    available_seats = Column(Integer)
    bookings = relationship("Booking", back_populates="movie")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    booking_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    seats = Column(Integer)
    user = relationship("User", back_populates="bookings")
    movie = relationship("Movie", back_populates="bookings")
