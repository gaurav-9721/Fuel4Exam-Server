# Fuel4Exam Backend - Development Guide

## Quick Start

### 1. Setup Environment

```bash
# Clone repository
git clone <repo-url>
cd Fuel4Exam-Server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your configuration
```

### 2. Initialize Database

```bash
# Seed database with sample data
python seed.py

# Or run manually
python -c "from app.db.session import init_db; init_db()"
```

### 3. Run Application

```bash
# Development mode with auto-reload
python main.py

# Or using Uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Visit: `http://localhost:8000`
- API Docs: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

---

## Architecture Overview

### Layered Architecture

```
┌─────────────────────────────────────┐
│        API Routers & Endpoints      │  (Request handlers)
│         /app/api/v1/endpoints       │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│        Services (Business Logic)    │  (Domain logic, validation)
│         /app/services               │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│    Database (Models & Session)      │  (Data access)
│         /app/db                     │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│      PostgreSQL (Neon Cloud)        │  (Persistence)
└─────────────────────────────────────┘
```

### Module Responsibilities

| Module | Responsibility |
|--------|-----------------|
| `core/` | Configuration, security, JWT |
| `db/` | Database models and sessions |
| `schemas/` | Request/response validation (Pydantic) |
| `services/` | Business logic and domain operations |
| `api/` | HTTP endpoints and routers |
| `exceptions/` | Custom exception definitions |
| `utils/` | Utility functions and logging |

---

## Authentication Flow

### Registration

```
User Request (POST /api/v1/auth/register)
    ↓
AuthService.register_user()
    ├─ Check email/username uniqueness
    ├─ Hash password with bcrypt
    ├─ Create User in database
    └─ Generate JWT tokens
    ↓
Response with access_token + refresh_token
```

### Login

```
User Request (POST /api/v1/auth/login)
    ↓
AuthService.login_user()
    ├─ Find user by email
    ├─ Verify password
    ├─ Update last_login_at
    └─ Generate JWT tokens
    ↓
Response with access_token + refresh_token
```

### Token Verification

```
API Request with Authorization Header
    ↓
Extract Bearer token
    ↓
jwt_handler.verify_token()
    ├─ Decode JWT signature
    ├─ Check expiration
    ├─ Extract user_id
    └─ Return payload
    ↓
Proceed or return 401 Unauthorized
```

---

## API Endpoints Reference

### Authentication Endpoints

#### Register User
```
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "SecurePassword123",
  "first_name": "John",
  "last_name": "Doe"
}

Response 201:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "first_name": "John",
    "last_name": "Doe",
    "role": "student",
    "status": "active",
    "created_at": "2024-01-01T12:00:00"
  }
}
```

#### Login
```
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123"
}

Response 200: [Same as register]
```

#### Refresh Token
```
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response 200:
{
  "access_token": "new_token...",
  "refresh_token": "new_refresh_token...",
  "token_type": "bearer",
  "expires_in": 30
}
```

### User Profile Endpoints

#### Get Current User Profile
```
GET /api/v1/users/me
Authorization: Bearer <access_token>

Response 200:
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Software developer",
  "profile_picture_url": "https://...",
  "phone_number": "+1234567890",
  "role": "student",
  "status": "active",
  "is_email_verified": true,
  "is_active": true,
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-02T12:00:00",
  "last_login_at": "2024-01-02T12:30:00"
}
```

#### Get User by ID
```
GET /api/v1/users/{user_id}

Response 200: [Same as above]
```

#### Update Profile
```
PUT /api/v1/users/me
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "Jane",
  "bio": "Updated bio",
  "phone_number": "+9876543210"
}

Response 200: [Updated user profile]
```

#### Deactivate Account
```
POST /api/v1/users/me/deactivate
Authorization: Bearer <access_token>

Response 200:
{
  "message": "Account deactivated successfully",
  "success": true
}
```

---

## Adding New Features

### Step 1: Create Schema (if needed)
```python
# app/schemas/exam.py
from pydantic import BaseModel

class ExamCreate(BaseModel):
    title: str
    description: str
```

### Step 2: Create Database Model (if needed)
```python
# app/db/models.py
class Exam(Base):
    __tablename__ = "exams"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    # ... other fields
```

### Step 3: Create Service
```python
# app/services/exam/exam_service.py
class ExamService:
    @staticmethod
    def create_exam(db: Session, exam_data: ExamCreate) -> Exam:
        # Business logic here
        pass
```

### Step 4: Create API Endpoint
```python
# app/api/v1/endpoints/exams.py
from fastapi import APIRouter

router = APIRouter(prefix="/exams", tags=["Exams"])

@router.post("/", response_model=ExamResponse)
def create_exam(exam_data: ExamCreate, db: Session = Depends(get_db)):
    return ExamService.create_exam(db, exam_data)
```

### Step 5: Include Router in API
```python
# app/api/v1/api.py
from app.api.v1.endpoints import exams
api_router.include_router(exams.router)
```

---

## Error Handling

### Exception Hierarchy

```
Fuel4ExamException (Base)
├── AuthenticationException (401)
├── AuthorizationException (403)
├── UserNotFoundException (404)
├── UserAlreadyExistsException (409)
├── InvalidCredentialsException (401)
├── InvalidTokenException (401)
├── ValidationException (422)
└── DatabaseException (500)
```

### Usage Example

```python
from app.exceptions.exceptions import UserNotFoundException

try:
    user = UserService.get_user_by_id(db, user_id)
except UserNotFoundException as e:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=e.message
    )
```

---

## Testing

### Unit Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::test_register_user
```

### Integration Tests
```bash
# Run integration tests
pytest tests/integration/

# With database
pytest --db postgresql://...
```

---

## Database Migrations

Using Alembic for schema management:

```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add email_verified column"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1

# Check current revision
alembic current
```

---

## Deployment

### Docker Deployment

```bash
# Build image
docker build -t fuel4exam-api .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  -e SECRET_KEY="your-secret-key" \
  fuel4exam-api

# Using docker-compose
docker-compose up -d
```

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY` (32+ characters)
- [ ] Configure proper database backups
- [ ] Setup SSL/TLS certificates
- [ ] Configure reverse proxy (Nginx)
- [ ] Setup monitoring and logging
- [ ] Configure rate limiting
- [ ] Setup health checks
- [ ] Test disaster recovery
- [ ] Document runbooks

---

## Environment Variables

```
DATABASE_URL          # PostgreSQL connection string
SECRET_KEY            # JWT signing key (min 32 chars)
ALGORITHM             # JWT algorithm (default: HS256)
ACCESS_TOKEN_EXPIRE_MINUTES    # Access token TTL
REFRESH_TOKEN_EXPIRE_DAYS      # Refresh token TTL
DEBUG                 # Debug mode (False in production)
ENVIRONMENT           # Environment name
ALLOWED_ORIGINS       # CORS allowed origins
APP_NAME             # Application name
APP_VERSION          # Application version
```

---

## Performance Optimization

### Database
- Use connection pooling (already configured)
- Add database indexes on frequently queried columns
- Use pagination for list endpoints
- Monitor slow queries

### Caching
- Implement Redis caching for user sessions
- Cache frequently accessed data
- Set appropriate TTLs

### API
- Add request rate limiting
- Implement pagination
- Compress responses (gzip)
- Use CDN for static assets

---

## Security Best Practices

1. **Secrets Management**
   - Use environment variables
   - Never commit secrets
   - Rotate keys regularly

2. **Password Security**
   - Minimum 8 characters
   - Hashed with bcrypt
   - Salt automatically included

3. **Token Security**
   - Short expiration times
   - Refresh token rotation
   - HTTPS only in production

4. **Input Validation**
   - Pydantic schemas validate all input
   - Email validation
   - Username format validation

5. **Database Security**
   - SSL/TLS connections required
   - Connection pooling
   - SQL injection prevention (ORM)

---

## Logging

### Log Levels
- **DEBUG**: Development details
- **INFO**: General information
- **WARNING**: Warning messages
- **ERROR**: Error messages
- **CRITICAL**: Critical errors

### Accessing Logs
```bash
# View logs in container
docker logs -f <container_id>

# View application logs
tail -f logs/fuel4exam.log

# Search logs
grep "error" logs/fuel4exam.log
```

---

## Monitoring & Health Checks

### Health Check Endpoint
```
GET /health
Response:
{
  "status": "healthy",
  "service": "Fuel4Exam",
  "version": "1.0.0",
  "environment": "production"
}
```

### Metrics to Monitor
- Request count and latency
- Error rates
- Database connection pool
- JWT token validation
- User registration/login rates

---

## Troubleshooting

### Common Issues

**Issue**: Database connection failed
```
Solution: Check DATABASE_URL, verify network connectivity,
          confirm SSL certificates if required
```

**Issue**: JWT token invalid
```
Solution: Verify SECRET_KEY matches, check token expiration,
          ensure correct algorithm specified
```

**Issue**: CORS errors
```
Solution: Check ALLOWED_ORIGINS configuration,
          verify client origin matches allowed list
```

---

## Contributing

1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes following the architecture
3. Write tests
4. Submit pull request with description
5. Code review and merge

---

## Support

For issues, create a GitHub issue or contact the development team.
