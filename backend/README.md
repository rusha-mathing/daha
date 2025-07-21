# Daha Admin API

A FastAPI-based REST API for managing educational courses, subjects, and resources.

## Features

- **Authentication**: JWT-based authentication with role-based access control
- **Course Management**: CRUD operations for courses with filtering
- **Subject Management**: Manage educational subjects and categories
- **User Management**: User registration, login, and profile management
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Validation**: Comprehensive input validation with Pydantic

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL
- pip or uv

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Set up the database:
   ```bash
   # Create PostgreSQL database
   createdb daha_db
   
   # Run migrations
   python -c "from app.models import create_db_and_models; import asyncio; asyncio.run(create_db_and_models())"
   ```

5. Run the server:
   ```bash
   python main.py
   ```

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token
- `GET /auth/me` - Get current user info
- `PUT /auth/me` - Update current user
- `POST /auth/change-password` - Change password

### Courses

- `GET /courses/` - Get all courses with filtering
- `GET /courses/{id}` - Get course by ID
- `POST /courses/` - Create new course
- `PUT /courses/{id}` - Update course
- `DELETE /courses/{id}` - Delete course

### Subjects

- `GET /subjects/` - Get all subjects
- `GET /subjects/{id}` - Get subject by ID
- `POST /subjects/` - Create new subject
- `PUT /subjects/{id}` - Update subject
- `DELETE /subjects/{id}` - Delete subject

### Difficulties

- `GET /difficulties/` - Get all difficulties
- `GET /difficulties/{id}` - Get difficulty by ID
- `POST /difficulties/` - Create new difficulty
- `PUT /difficulties/{id}` - Update difficulty
- `DELETE /difficulties/{id}` - Delete difficulty

## Configuration

The application uses environment variables for configuration:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost/daha_db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Environment
ENVIRONMENT=development
DEBUG=true
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Install development dependencies
pip install black isort mypy

# Format code
black .
isort .

# Type checking
mypy .
```

## Deployment

### Docker

```bash
docker build -t daha-api .
docker run -p 8000:8000 daha-api
```

### Production

1. Set `ENVIRONMENT=production`
2. Use a strong `SECRET_KEY`
3. Configure proper CORS origins
4. Set up a production database
5. Use a reverse proxy (nginx)
6. Set up SSL/TLS certificates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request
