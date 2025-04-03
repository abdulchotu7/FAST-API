from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, auth
from .database import engine, Base, get_db
from .config import settings
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: Add cleanup code here if needed
    pass

app = FastAPI(
    title="Movie Booking API",
    description="A simple FastAPI-based movie ticket booking system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"status": "success", "message": "Movie Booking API is running"}

# Auth routes
@app.post("/auth/signup", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered"
        )

    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/auth/create-admin", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    # Check if the admin key matches the one in the environment
    if admin.admin_key != settings.ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin key"
        )

    db_user = db.query(models.User).filter(models.User.username == admin.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered"
        )

    hashed_password = auth.get_password_hash(admin.password)
    db_user = models.User(username=admin.username, password=hashed_password, is_admin=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/auth/login", response_model=schemas.Token)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.create_access_token(
        data={"sub": user.username},
        user_is_admin=user.is_admin
    )

    auth.set_auth_cookie(response, access_token)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Successfully logged out"}

@app.post("/admin/movies", response_model=schemas.Movie, status_code=status.HTTP_201_CREATED)
def create_movie(
    movie: schemas.MovieCreate,
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db)
):
    db_movie = models.Movie(
        title=movie.title,
        showtime=movie.showtime,
        available_seats=movie.available_seats
    )

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return db_movie

@app.get("/movies", response_model=List[schemas.Movie])
def view_movies(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(models.Movie).all()

@app.post("/movies/{movie_id}/book", response_model=schemas.Booking)
def book_movie(
    movie_id: int,
    booking: schemas.BookingCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )

    if movie.available_seats < booking.seats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {movie.available_seats} seats available"
        )

    db_booking = models.Booking(
        user_id=current_user.id,
        movie_id=movie_id,
        seats=booking.seats
    )
    movie.available_seats -= booking.seats

    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@app.get("/movies/history", response_model=List[schemas.Booking])
def view_history(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(models.Booking).filter(models.Booking.user_id == current_user.id).all()

@app.get("/auth/me", response_model=schemas.User)
def get_current_user_info(current_user: models.User = Depends(auth.get_current_user)):
    return current_user
