# Fuel4Exam Project Structure

## Complete Directory Tree

```
Fuel4Exam-Server/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   │
│   ├── core/                     # Core configuration & security
│   │   ├── __init__.py
│   │   ├── config.py            # Pydantic settings management
│   │   ├── security.py          # Password hashing utilities
│   │   └── jwt_handler.py       # JWT token operations
│   │
│   ├── db/                       # Database layer
│   │   ├── __init__.py
│   │   ├── session.py           # SQLAlchemy session & engine
│   │   └── models.py            # ORM models (User, etc)
│   │
│   ├── schemas/                  # Pydantic schemas
│   │   ├── __init__.py
│   │   └── user.py              # User schemas (Register, Login, etc)
│   │
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth/                # Authentication service
│   │   │   ├── __init__.py
│   │   │   └── auth_service.py
│   │   └── user/                # User management service
│   │       ├── __init__.py
│   │       └── user_service.py
│   │
│   ├── api/                      # API routers & endpoints
│   │   ├── __init__.py
│   │   └── v1/                  # API v1
│   │       ├── __init__.py
│   │       ├── api.py           # Router aggregator
│   │       └── endpoints/       # Endpoint modules
│   │           ├── __init__.py
│   │           ├── auth.py      # Auth endpoints
│   │           └── users.py     # User endpoints
│   │
│   ├── exceptions/               # Custom exceptions
│   │   ├── __init__.py
│   │   └── exceptions.py        # Exception classes
│   │
│   └── utils/                    # Utilities
│       ├── __init__.py
│       └── logging.py           # Logging configuration
│
├── main.py                       # Application entry point script
├── seed.py                       # Database seeding utility
│
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
│
├── Dockerfile                    # Docker image definition
├── docker-compose.yml            # Docker compose configuration
│
├── README.md                     # Project overview & setup
├── DEVELOPMENT.md                # Development guide & best practices
├── API_DOCUMENTATION.md          # API endpoints reference
├── PROJECT_STRUCTURE.md          # This file
│
└── [other git files]
```

---

## Module Descriptions

### `app/core/`
**Purpose:** Core application configuration and security

- **config.py**: Loads environment variables into Pydantic Settings
- **security.py**: Password hashing and verification using bcrypt
- **jwt_handler.py**: JWT token creation, verification, and decoding

### `app/db/`
**Purpose:** Database abstraction layer

- **session.py**: SQLAlchemy engine, session management, connection pooling
- **models.py**: SQLAlchemy ORM models (User with full schema)

### `app/schemas/`
**Purpose:** Request/Response validation

- **user.py**: Pydantic models for user registration, login, profile updates, responses

### `app/services/`
**Purpose:** Business logic and domain operations

- **auth/auth_service.py**: Register, login, token generation, verification
- **user/user_service.py**: Profile operations, activation/deactivation

### `app/api/`
**Purpose:** HTTP request handlers

- **v1/endpoints/auth.py**: `/auth/register`, `/auth/login`, `/auth/refresh`
- **v1/endpoints/users.py**: `/users/me`, `/users/{id}`, profile updates
- **v1/api.py**: Combines all routers for v1

### `app/exceptions/`
**Purpose:** Custom exception hierarchy

- **exceptions.py**: Application-specific exception classes with HTTP status codes

### `app/utils/`
**Purpose:** Utility functions

- **logging.py**: Structured logging configuration

---

## Data Flow Examples

### User Registration Flow
```
POST /api/v1/auth/register
  ↓
[Pydantic validation via UserRegister schema]
  ↓
auth_service.register_user()
  ├─ Check if email/username exists
  ├─ Hash password with bcrypt
  ├─ Create User in database
  └─ Generate JWT tokens
  ↓
Response: AuthResponse with tokens + user data
```

### User Login Flow
```
POST /api/v1/auth/login
  ↓
[Pydantic validation via UserLogin schema]
  ↓
auth_service.login_user()
  ├─ Find user by email
  ├─ Verify password
  ├─ Update last_login_at
  └─ Generate tokens
  ↓
Response: AuthResponse with tokens + user data
```

### Protected Request Flow
```
GET /api/v1/users/me (with Authorization header)
  ↓
Extract Bearer token from header
  ↓
get_current_user_from_header() dependency
  ├─ Verify token with jwt_handler.verify_token()
  ├─ Extract user_id from token
  └─ Fetch user from database
  ↓
Return user profile if valid, 401 if invalid
```

---

## Key Technologies

| Component | Technology | Version |
|-----------|-----------|---------|
| Web Framework | FastAPI | 0.104.1 |
| ASGI Server | Uvicorn | 0.24.0 |
| ORM | SQLAlchemy | 2.0.23 |
| Database | PostgreSQL (Neon) | Cloud |
| Validation | Pydantic | 2.5.0 |
| Authentication | JWT (python-jose) | 3.3.0 |
| Password Hashing | bcrypt (via passlib) | 1.7.4 |
| Database Driver | psycopg2 | 2.9.9 |
| Migrations | Alembic | 1.13.0 |

---

## Database Schema

### User Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    
    bio TEXT,
    profile_picture_url VARCHAR(255),
    phone_number VARCHAR(20),
    
    role ENUM('student', 'instructor', 'admin'),
    status ENUM('active', 'inactive', 'suspended'),
    is_email_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP NULL
);
```

---

## Configuration Management

### Environment Variables
```
DATABASE_URL              # PostgreSQL connection
SECRET_KEY               # JWT signing key
ALGORITHM                # JWT algorithm
ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS
DEBUG                    # Debug mode
ENVIRONMENT              # Deployment environment
ALLOWED_ORIGINS          # CORS origins
APP_NAME                 # Application name
APP_VERSION              # Version number
```

### Loading Mechanism
```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    # ... other fields

settings = Settings()  # Loads from .env
```

---

## API Versioning Strategy

Current: `/api/v1`

Future versions can be added:
- `/api/v2/` - Separate router
- `/api/v3/` - New endpoints

Backward compatibility maintained through version-specific endpoints.

---

## Security Layers

1. **Input Validation**: Pydantic schemas validate all inputs
2. **Password Security**: Bcrypt hashing with salt
3. **Token Security**: JWT with expiration times
4. **Database Security**: SSL/TLS connections, connection pooling
5. **CORS**: Configured allowed origins only
6. **Exception Handling**: No sensitive info in error messages

---

## Error Handling Strategy

```
Exception occurs
  ↓
Custom exception handler catches it
  ↓
Logs error with appropriate level
  ↓
Returns JSON response with status code
  ↓
No sensitive info leaked in response
```

---

## Deployment Layers

### Development
```bash
python main.py
# or
uvicorn app.main:app --reload
```

### Docker
```bash
docker build -t fuel4exam-api .
docker run -p 8000:8000 fuel4exam-api
```

### Docker Compose
```bash
docker-compose up -d
```

### Production (Gunicorn + Nginx)
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
# Behind Nginx reverse proxy with SSL
```

---

## Testing Structure (To Be Added)

```
tests/
├── __init__.py
├── conftest.py           # Pytest configuration & fixtures
├── unit/
│   ├── test_auth_service.py
│   ├── test_user_service.py
│   └── test_security.py
├── integration/
│   ├── test_auth_endpoints.py
│   ├── test_user_endpoints.py
│   └── test_db_operations.py
└── e2e/
    └── test_complete_workflow.py
```

---

## Performance Considerations

### Database
- Connection pooling (20 connections)
- `pool_pre_ping=True` for connection health
- Indexes on email, username columns
- Pagination for list endpoints (future)

### Caching (Future)
- Redis for session caching
- User profile caching with TTL
- Token blacklist caching

### API
- Compression via middleware
- Request rate limiting (future)
- Response pagination (future)
- Database query optimization

---

## Monitoring & Logging

### Log Outputs
- Console: Standard application logs
- File: Detailed logs in `logs/fuel4exam.log`

### Health Check
```
GET /health
→ Returns service status, version, environment
```

### Metrics to Monitor
- Request count and latency
- Error rates
- Database connection pool usage
- User registration/login rates
- Token validation failures

---

## Scalability Plan

### Horizontal Scaling
1. Load balancer (Nginx, HAProxy)
2. Multiple API instances
3. Shared PostgreSQL database
4. Redis for session sharing

### Vertical Scaling
1. Increase server resources
2. Database query optimization
3. Caching layer implementation
4. Background job processing

### Database Scaling
1. Read replicas for reports
2. Sharding if needed
3. Connection pooling optimization
4. Query caching

---

## Migration Path

### Current (MVP)
- Basic authentication
- User profiles
- JWT tokens

### Phase 2 (Q2 2024)
- Email verification
- Password reset
- Two-factor authentication

### Phase 3 (Q3 2024)
- Exam management
- Question bank
- User progress tracking

### Phase 4 (Q4 2024)
- AI/LLM integration
- Advanced analytics
- Admin dashboard

---

## File Naming Conventions

- **Models**: `models.py` (plurals for table names: `User` → `users`)
- **Services**: `*_service.py` (e.g., `auth_service.py`)
- **Schemas**: `user.py`, `exam.py` (entity name)
- **Endpoints**: `auth.py`, `users.py` (plural for collections)
- **Tests**: `test_*.py`
- **Constants**: `UPPERCASE` variable names

---

## Code Style Guidelines

- Python: PEP 8 (via Black formatter)
- Max line length: 100 characters
- Type hints for all functions
- Docstrings for all modules and functions
- Exception handling: Specific exceptions before generic

---

## Key Decisions

1. **Pydantic v2**: Type safety and validation
2. **SQLAlchemy ORM**: Type safety, relationship management
3. **JWT over Sessions**: Stateless, scalable authentication
4. **Layered Architecture**: Separation of concerns
5. **Environment-based Configuration**: Flexibility across environments

---

## Future Enhancements

- [ ] Database migrations (Alembic)
- [ ] Comprehensive test suite
- [ ] API rate limiting
- [ ] Caching layer (Redis)
- [ ] WebSocket support
- [ ] GraphQL option
- [ ] Mobile API (similar structure)
- [ ] Admin API endpoints
- [ ] Analytics and reporting

---

## Support & Documentation

- **README.md**: Project overview and setup
- **DEVELOPMENT.md**: Development guide and best practices
- **API_DOCUMENTATION.md**: Complete API reference
- **PROJECT_STRUCTURE.md**: This file - architecture overview

For detailed information on specific components, refer to inline code documentation.
