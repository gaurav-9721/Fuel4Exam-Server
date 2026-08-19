# Fuel4Exam - Backend Server

Production-grade exam preparation backend system built with FastAPI, SQLAlchemy, and PostgreSQL.

## Project Structure

```
app/
├── __init__.py
├── main.py                 # FastAPI application entry point
├── core/                   # Core configuration and security
│   ├── __init__.py
│   ├── config.py          # Settings and configuration
│   ├── security.py        # Password hashing
│   └── jwt_handler.py     # JWT token generation and validation
├── db/                     # Database layer
│   ├── __init__.py
│   ├── session.py         # Database connection and session management
│   └── models.py          # SQLAlchemy ORM models
├── schemas/                # Pydantic validation schemas
│   ├── __init__.py
│   └── user.py            # User-related schemas
├── services/               # Business logic layer
│   ├── __init__.py
│   ├── auth/              # Authentication services
│   │   ├── __init__.py
│   │   └── auth_service.py
│   └── user/              # User profile services
│       ├── __init__.py
│       └── user_service.py
├── api/                    # API routers and endpoints
│   ├── __init__.py
│   └── v1/                # API version 1
│       ├── __init__.py
│       ├── api.py         # Router aggregator
│       └── endpoints/
│           ├── __init__.py
│           ├── auth.py    # Authentication endpoints
│           └── users.py   # User profile endpoints
├── exceptions/             # Custom exceptions
│   ├── __init__.py
│   └── exceptions.py
└── utils/                  # Utility functions
    ├── __init__.py
    └── logging.py         # Logging configuration

main.py                    # Entry point script
requirements.txt           # Python dependencies
.env.example              # Environment variables example
.gitignore
```

## Features Implemented

### Authentication
- User registration with email validation
- User login with email and password
- JWT-based access and refresh tokens
- Token refresh mechanism
- Secure password hashing with bcrypt

### User Management
- Get user profile
- Update user profile
- Deactivate/Activate user account
- Email verification status
- User role management (Student, Instructor, Admin)
- User status management (Active, Inactive, Suspended)

### Database
- PostgreSQL with Neon cloud database
- SQLAlchemy ORM with proper relationships
- Connection pooling and session management
- Automatic timestamp management (created_at, updated_at, last_login_at)

### API Design
- RESTful API design
- Comprehensive error handling
- Request/Response validation with Pydantic
- API versioning (v1)
- Swagger/OpenAPI documentation
- CORS support

### Security
- JWT token-based authentication
- Password hashing with bcrypt
- Environment-based configuration
- Exception handling and logging

## Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL (using Neon cloud database)
- pip or conda

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd Fuel4Exam-Server
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application
```bash
python main.py
```

The API will be available at `http://localhost:8000`
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user

### User Profile
- `GET /api/v1/users/me` - Get current user profile
- `GET /api/v1/users/{user_id}` - Get user profile by ID
- `PUT /api/v1/users/me` - Update current user profile
- `POST /api/v1/users/me/deactivate` - Deactivate user account

## Database Access

### Cloud Database (Neon)
The application uses Neon PostgreSQL cloud database. To access:

1. **Connection String**: The connection string is configured in `.env` file
2. **Neon Console**: Visit https://console.neon.tech
3. **Database Tools**: Use pgAdmin or any PostgreSQL client
   - Host: `ep-lively-art-azfphgc0-pooler.c-3.ap-southeast-1.aws.neon.tech`
   - Database: `fuel4exam`
   - User: `neondb_owner`
   - Port: `5432`

### Using psql
```bash
psql "$DATABASE_URL"
```

## Environment Variables

See `.env.example` for all configuration options:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token expiration (30 minutes)
- `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiration (7 days)
- `DEBUG`: Debug mode (False in production)
- `ENVIRONMENT`: Environment name (production/development)
- `ALLOWED_ORIGINS`: CORS allowed origins

## Documentation

- [Quickstart](docs/QUICKSTART.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [API Documentation](docs/API_DOCUMENTATION.md)
- [Project Structure](docs/PROJECT_STRUCTURE.md)
- [Implementation Summary](docs/IMPLEMENTATION_SUMMARY.md)

## Future Enhancements

- [ ] LLM integration for AI-based exam services
- [ ] Exam question management
- [ ] User exam results and analytics
- [ ] Notification system
- [ ] Payment integration
- [ ] Admin dashboard
- [ ] Email verification service
- [ ] Two-factor authentication
- [ ] Advanced user roles and permissions
- [ ] Exam scheduling system

## Development

### Running Tests
```bash
pytest
```

### Database Migrations
```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Logging
Logs are configured to output to console and file (`logs/fuel4exam.log`)

## Production Deployment

1. Update `.env` with production settings
2. Set `DEBUG=False`
3. Use strong `SECRET_KEY`
4. Use production ASGI server (Gunicorn, Uvicorn)
5. Configure reverse proxy (Nginx)
6. Setup SSL/TLS certificates
7. Monitor application logs and performance

## License

Proprietary - Fuel4Exam

## Support

For issues and questions, contact the development team.
Fuel your preparation, Fuel your future
