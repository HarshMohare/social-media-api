# Social Media API

A REST API built with FastAPI and PostgreSQL.

## Features
- JWT Authentication
- CRUD operations for Posts
- Voting system (Like/Unlike)
- User management

## Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT (PyJWT)

## Installation

1. Clone the repository
```bash
git clone https://github.com/HarshMohare/social-media-api.git
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create `.env` file

DATABASE_URL=postgresql://username:password@localhost:5432/dbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

4. Run the server
```bash
uvicorn app.main:app --reload
```

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | /users/ | Register |
| POST | /login | Login |
| GET | /posts/ | Get all posts |
| POST | /posts/ | Create post |
| GET | /posts/{id} | Get post |
| PUT | /posts/{id} | Update post |
| DELETE | /posts/{id} | Delete post |
| POST | /vote/ | Vote on post |
