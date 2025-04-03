from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, auth
from .database import engine, Base, get_db
from sqlalchemy import select, func

app = FastAPI()

# Create tables at startup
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}  # Changed to match the test

# Auth routes
@app.post("/auth/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = models.User(username=user.username, password=user.password)
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
    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()
    
    if not user or user.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(
        data={"sub": user.username},
        user_is_admin=user.is_admin
    )
    
    # Set the cookie
    auth.set_auth_cookie(response, access_token)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Successfully logged out"}

# Admin routes
@app.post("/admin/movies", response_model=schemas.Movie)
def create_movie(
    movie: schemas.MovieCreate,
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db)
):
    try:
        # Convert Pydantic model to dict and create Movie instance
        movie_data = movie.dict()
        db_movie = models.Movie(
            title=movie_data["title"],
            showtime=movie_data["showtime"],
            available_seats=movie_data["available_seats"]
        )
        
        # Add to session and commit
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        
        return db_movie
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create movie: {str(e)}"
        )

@app.get("/admin/movies", response_model=List[schemas.Movie])
def get_all_movies(
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db)
):
    return db.query(models.Movie).all()

# User routes
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
        raise HTTPException(status_code=404, detail="Movie not found")
    if movie.available_seats < booking.seats:
        raise HTTPException(status_code=400, detail="Not enough seats available")
    
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

# Debug endpoint to check current user's details
@app.get("/auth/me", response_model=schemas.User)
def get_current_user_info(current_user: models.User = Depends(auth.get_current_user)):
    return current_user
