from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    is_admin: Optional[bool] = None

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True

class CurrentUser(BaseModel):
    username: str
    is_admin: bool

    class Config:
        orm_mode = True

class MovieBase(BaseModel):
    title: str
    showtime: datetime
    available_seats: int

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True

class BookingBase(BaseModel):
    seats: int

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    user_id: int
    movie_id: int
    booking_time: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str
