# Movie Booking API

A simple FastAPI-based movie ticket booking system with user authentication and admin features.

## Quick Start

1. **Clone and Setup**
```bash
git clone https://github.com/abdulchotu7/FAST-API.git
cd FAST-API
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Create `.env` file**
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./sql_app.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. **Run the API**
```bash
uvicorn app.main:app --reload
```

## Features

- User authentication with JWT tokens
- Movie listing and booking
- Admin panel for movie management
- Secure booking system

## API Endpoints

### Public
- `POST /auth/login` - Login
- `GET /movies` - View movies
- `POST /movies/{id}/book` - Book tickets

### Admin Only
- `POST /admin/movies` - Add movie
- `PUT /admin/movies/{id}` - Update movie
- `DELETE /admin/movies/{id}` - Delete movie

## Documentation

- API docs available at: `http://localhost:8000/docs`
- ReDoc available at: `http://localhost:8000/redoc`

## Project Structure
```
app/
├── main.py      # FastAPI app and routes
├── models.py    # Database models
├── auth.py      # Authentication logic
└── database.py  # Database setup
```

## Requirements

See `requirements.txt` for full list:
- fastapi
- uvicorn
- sqlalchemy
- python-jose
- passlib
- python-dotenv

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Abdul Rahim - [@abdulchotu7](https://github.com/abdulchotu7)

Project Link: [https://github.com/abdulchotu7/FAST-API](https://github.com/abdulchotu7/FAST-API)
