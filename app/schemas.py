from pydantic import BaseModel, ConfigDict, field_validator
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

class AdminCreate(UserCreate):
    admin_key: str

class User(UserBase):
    id: int
    is_admin: bool
    model_config = ConfigDict(from_attributes=True)

class MovieBase(BaseModel):
    title: str
    showtime: datetime
    available_seats: int

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class BookingBase(BaseModel):
    seats: int

    @field_validator('seats')
    @classmethod
    def validate_seats(cls, v):
        if v <= 0:
            raise ValueError('Number of seats must be positive')
        return v

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    user_id: int
    movie_id: int
    booking_time: datetime
    model_config = ConfigDict(from_attributes=True)
