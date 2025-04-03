from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Token schemas for OAuth2
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    is_admin: Optional[bool] = None

# User schemas
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

# Movie schemas
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

# Booking schemas
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

# For OAuth2 password flow
class UserLogin(BaseModel):
    username: str
    password: str
