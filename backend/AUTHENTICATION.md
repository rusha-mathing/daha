# 🔐 Authentication & Authorization System

This document describes the JWT-based authentication system implemented for the Daha backend.

## 📋 Overview

The authentication system provides:
- **JWT-based authentication** with secure token management
- **Role-based authorization** (Admin, Moderator, User)
- **Password hashing** with bcrypt
- **Session management** with token expiration
- **Protected endpoints** with role-based access control

## 🏗️ Architecture

### Database Schema
```sql
-- Users table
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR,
    role VARCHAR NOT NULL DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

-- User sessions table (for token management)
CREATE TABLE user_session (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user(id),
    token_hash VARCHAR UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);
```

### User Roles
- **ADMIN**: Full system access, user management
- **MODERATOR**: Course management, content moderation
- **USER**: Basic access, view courses

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create `.env` file:
```env
# Database
DATABASE_URL=postgresql+asyncpg://daha_user:SWP2025@localhost/daha_db

# JWT Settings
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Security
BCRYPT_ROUNDS=12
```

### 3. Initialize Database
```bash
python -c "from app.models import create_db_and_models; import asyncio; asyncio.run(create_db_and_models())"
```

## 📡 API Endpoints

### Authentication Endpoints

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
    "email": "user@example.com",
    "username": "username",
    "password": "securepassword",
    "full_name": "John Doe",
    "role": "user"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword"
}
```

Response:
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer",
    "expires_in": 1800,
    "user": {
        "id": 1,
        "email": "user@example.com",
        "username": "username",
        "full_name": "John Doe",
        "role": "user",
        "is_active": true,
        "created_at": "2024-01-01T00:00:00",
        "last_login": "2024-01-01T12:00:00"
    }
}
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer <access_token>
```

#### Update User Profile
```http
PUT /auth/me
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "full_name": "John Smith",
    "email": "newemail@example.com"
}
```

#### Change Password
```http
POST /auth/change-password
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "current_password": "oldpassword",
    "new_password": "newpassword"
}
```

### Admin Endpoints

#### Get All Users
```http
GET /auth/users
Authorization: Bearer <admin_token>
```

#### Update User Role
```http
PUT /auth/users/{user_id}/role
Authorization: Bearer <admin_token>
Content-Type: application/json

{
    "role": "moderator"
}
```

#### Toggle User Active Status
```http
PUT /auth/users/{user_id}/toggle-active
Authorization: Bearer <admin_token>
```

## 🛡️ Protected Endpoints

### Admin-Only Endpoints
```python
# Example: Create subject (admin only)
@router.post('/subjects/')
async def create_subject(
    subject: SubjectCreate,
    current_user: User = Depends(auth_service.require_role(UserRole.ADMIN))
):
    # Only admins can access this endpoint
    pass
```

### Moderator-Or-Admin Endpoints
```python
# Example: Create course (moderator or admin)
@router.post('/courses/')
async def create_course(
    course: CourseCreate,
    current_user: User = Depends(auth_service.require_role(UserRole.MODERATOR))
):
    # Moderators and admins can access this endpoint
    pass
```

### Any Authenticated User
```python
# Example: Get user profile
@router.get('/me')
async def get_profile(
    current_user: User = Depends(auth_service.get_current_user)
):
    # Any authenticated user can access this endpoint
    pass
```

## 🔧 Configuration

### Security Settings
```python
# In app/auth/services.py
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
```

### Password Security
- **Hashing**: bcrypt with 12 rounds
- **Validation**: Minimum 8 characters
- **Storage**: Hashed passwords only

### Token Security
- **Algorithm**: HS256
- **Expiration**: 30 minutes (access), 7 days (refresh)
- **Storage**: Database with hash tracking

## 🚨 Security Best Practices

### 1. Environment Variables
```bash
# Never commit secrets to version control
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/db
```

### 2. Token Management
- Tokens expire automatically
- Refresh tokens for long-term sessions
- Database tracking of active sessions

### 3. Role-Based Access
- Always verify user roles
- Use dependency injection for protection
- Log access attempts

### 4. Password Security
- Never store plain text passwords
- Use bcrypt for hashing
- Implement password complexity rules

## 🔍 Monitoring & Logging

### Authentication Events
```python
# Log successful logins
logger.info(f"User {user.email} logged in successfully")

# Log failed attempts
logger.warning(f"Failed login attempt for email: {email}")

# Log role changes
logger.info(f"User {user_id} role changed to {new_role}")
```

### Security Monitoring
- Track failed login attempts
- Monitor role changes
- Log suspicious activity

## 🧪 Testing

### Test Authentication
```bash
# Register a user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"password123"}'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Use token
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer <your_token>"
```

## 📚 Integration Examples

### Frontend Integration
```javascript
// Login function
async function login(email, password) {
    const response = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    
    const data = await response.json();
    localStorage.setItem('token', data.access_token);
    return data;
}

// Protected request
async function fetchProtectedData() {
    const token = localStorage.getItem('token');
    const response = await fetch('/admin/courses', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.json();
}
```

### Bot Integration
```python
# In your bot code
async def get_user_from_token(token: str):
    payload = auth_service.verify_token(token)
    if payload:
        user_id = payload.get("sub")
        return await get_user_by_id(user_id)
    return None
```

## 🚀 Deployment

### 1. Production Settings
```env
# Production environment variables
SECRET_KEY=<generate-secure-key>
DATABASE_URL=<production-db-url>
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30
```

### 2. Database Migration
```bash
# Run database migrations
alembic upgrade head
```

### 3. SSL/TLS
- Always use HTTPS in production
- Configure proper CORS settings
- Use secure cookies for sessions

## 🔄 Migration from Existing System

### 1. Add User Table
```sql
-- Add user table to existing database
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR,
    role VARCHAR NOT NULL DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);
```

### 2. Update Existing Endpoints
```python
# Before: Public endpoint
@router.post('/courses/')
async def create_course(course: CourseCreate):
    pass

# After: Protected endpoint
@router.post('/courses/')
async def create_course(
    course: CourseCreate,
    current_user: User = Depends(auth_service.require_role(UserRole.MODERATOR))
):
    pass
```

### 3. Frontend Updates
- Add login/register forms
- Implement token storage
- Add authorization headers to requests

## 📞 Support

For questions or issues with the authentication system:
1. Check the logs for error messages
2. Verify environment variables are set correctly
3. Ensure database tables are created
4. Test with the provided curl examples 