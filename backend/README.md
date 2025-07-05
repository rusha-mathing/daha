# Daha Backend API

A modern FastAPI-based backend for managing educational courses, subjects, and resources. This project provides a RESTful API with comprehensive CRUD operations, proper error handling, and extensive testing coverage.

## 🚀 Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **SQLModel ORM**: Type-safe database operations with SQLAlchemy
- **PostgreSQL Database**: Robust relational database support
- **Comprehensive Testing**: 51 tests including unit and integration tests
- **Middleware Support**: Logging and error handling middleware
- **CORS Support**: Cross-origin resource sharing configuration
- **Async/Await**: Full asynchronous support for better performance
- **Type Hints**: Complete type annotations for better code quality

## 📋 Prerequisites

- Python 3.12+
- PostgreSQL 12+
- pip or uv package manager

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd daha-vibe_improvements/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # Or using uv (recommended):
   uv sync
   ```

4. **Set up PostgreSQL**
   ```bash
   # Run the setup script
   chmod +x setup_postgres.sh
   ./setup_postgres.sh
   ```

5. **Configure environment variables**
   ```bash
   # Create .env file with your database configuration
   cp .env.example .env
   # Edit .env with your database credentials
   ```

## 🗄️ Database Setup

The application uses PostgreSQL with the following main entities:

- **Courses**: Educational courses with metadata
- **Subjects**: Course categories (AI, Programming, Robotics, etc.)
- **Organizations**: Educational institutions
- **Grades**: Target grade levels (7-11)
- **Difficulties**: Course difficulty levels (Beginner, Intermediate, Advanced)

### Database Schema

```sql
-- Main entities with relationships
courses (id, title, description, start_date, end_date, url, image_url, organization_id, difficulty_id)
subjects (id, type, label, icon, color, additional_description)
organizations (id, name)
grades (id, grade)
difficulties (id, type, label, icon, color)

-- Many-to-many relationships
course_subject_links (course_id, subject_id)
course_grade_links (course_id, grade_id)
```

## 🚀 Running the Application

### Development Mode
```bash
python main.py
```

### Production Mode
```bash
uvicorn main:api --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access:

- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Main Endpoints

#### Courses
- `GET /courses/` - List all courses (with pagination)
- `GET /courses/{id}/` - Get specific course
- `POST /courses/` - Create new course
- `PUT /courses/{id}/` - Update course
- `DELETE /courses/{id}/` - Delete course

#### Subjects
- `GET /subjects/` - List all subjects
- `GET /subjects/{id}/` - Get specific subject
- `POST /subjects/` - Create new subject
- `PUT /subjects/{id}/` - Update subject
- `DELETE /subjects/{id}/` - Delete subject

#### Organizations
- `GET /organizations/` - List all organizations
- `GET /organizations/{id}/` - Get specific organization
- `POST /organizations/` - Create new organization
- `PUT /organizations/{id}/` - Update organization
- `DELETE /organizations/{id}/` - Delete organization

#### Grades & Difficulties
- Similar CRUD operations for grades and difficulties

## 🧪 Testing

The project includes comprehensive testing with 51 tests:

### Running Tests
```bash
# Run all tests
python -m pytest app/ -v

# Run only unit tests
python -m pytest app/core/test_unit.py -v

# Run only integration tests
python -m pytest app/core/test_router.py -v

# Run with coverage
python -m pytest app/ --cov=app --cov-report=html
```

### Test Structure

#### Unit Tests (12 tests)
- **Services**: Business logic testing with mocked dependencies
- **Middleware**: Request/response processing testing
- **Exceptions**: Custom exception handling
- **Models**: Data validation and model behavior

#### Integration Tests (39 tests)
- **API Endpoints**: Full HTTP request/response testing
- **Database Operations**: Real database interactions
- **Error Scenarios**: 404, 422, 500 error handling
- **Data Relationships**: Many-to-many relationship testing

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── core/                 # Core application logic
│   │   ├── router.py        # Main API router
│   │   ├── services.py      # Business logic services
│   │   ├── middleware.py    # Custom middleware
│   │   ├── exceptions.py    # Custom exceptions
│   │   ├── models.py        # Database models
│   │   ├── config.py        # Configuration
│   │   ├── test_router.py   # Integration tests
│   │   └── test_unit.py     # Unit tests
│   ├── api.py              # FastAPI application factory
│   ├── models.py           # Database setup
│   └── router.py           # Router registration
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration
├── setup_postgres.sh      # Database setup script
├── create_mock_data.py    # Sample data generation
└── create_test_data.py    # Test data generation
```

## 🔧 Configuration

### Environment Variables
```bash
DATABASE_URL=postgresql+asyncpg://user:password@localhost/daha_db
DEBUG=True
LOG_LEVEL=INFO
```

### Database Configuration
The application supports both development and production database configurations through the `config.py` file.

## 🚀 Deployment

### Docker Deployment
```bash
# Build image
docker build -t daha-backend .

# Run container
docker run -p 8000:8000 daha-backend
```

### Production Considerations
- Use environment variables for sensitive data
- Configure proper CORS origins
- Set up database connection pooling
- Enable request logging and monitoring
- Use HTTPS in production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions
- Keep functions small and focused

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the test files for usage examples

## 🔄 API Versioning

The current API version is v1.0.0. Future versions will maintain backward compatibility where possible.

## 📊 Performance

- **Response Time**: Average < 100ms for simple queries
- **Database**: Optimized queries with proper indexing
- **Caching**: Ready for Redis integration
- **Async**: Non-blocking I/O operations

## 🔒 Security

- Input validation on all endpoints
- SQL injection protection through ORM
- CORS configuration for frontend integration
- Error handling without sensitive data exposure
