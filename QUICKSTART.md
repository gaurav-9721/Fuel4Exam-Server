# Fuel4Exam - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.9+
- PostgreSQL access (Neon cloud database provided)

---

## Step 1: Setup Environment (2 min)

```bash
# Clone/navigate to project
cd Fuel4Exam-Server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 2: Configure Environment (1 min)

```bash
# Copy example config
cp .env.example .env

# The .env already has the database connection
# No additional setup needed!
```

---

## Step 3: Initialize Database (1 min)

```bash
# Seed database with sample users
python seed.py

# Or just initialize tables
python -c "from app.db.session import init_db; init_db()"
```

**Sample Users Created:**
- Admin: `admin@fuel4exam.com` / `admin@123456`
- Instructor: `instructor@fuel4exam.com` / `instructor@123456`
- Student: `student@fuel4exam.com` / `student@123456`

---

## Step 4: Run Application (1 min)

```bash
python main.py
```

**Output:**
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Step 5: Test the API (instantly!)

### Option A: Swagger UI (Recommended)
Visit: **http://localhost:8000/api/docs**

Click "Try it out" on any endpoint!

### Option B: Using cURL

```bash
# Register new user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "username": "testuser",
    "password": "TestPass123",
    "first_name": "Test",
    "last_name": "User"
  }'

# Response:
# {
#   "access_token": "...",
#   "refresh_token": "...",
#   "token_type": "bearer",
#   "user": { ... }
# }

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "TestPass123"
  }'

# Get your profile (use access_token from login)
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Option C: Python Script

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Register
reg_response = requests.post(
    f"{BASE_URL}/auth/register",
    json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "TestPass123",
        "first_name": "John",
        "last_name": "Doe"
    }
)
print("Registration:", reg_response.json())

# Login
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "email": "test@example.com",
        "password": "TestPass123"
    }
)
token = login_response.json()["access_token"]
print("Token:", token)

# Get profile
profile_response = requests.get(
    f"{BASE_URL}/users/me",
    headers={"Authorization": f"Bearer {token}"}
)
print("Profile:", profile_response.json())
```

---

## API Endpoints Quick Reference

### Authentication
```
POST /api/v1/auth/register      → Create account
POST /api/v1/auth/login         → Login
POST /api/v1/auth/refresh       → Refresh token
GET  /api/v1/auth/me            → Current user
```

### User Profile
```
GET  /api/v1/users/me           → Get your profile
GET  /api/v1/users/{id}         → Get any user profile
PUT  /api/v1/users/me           → Update profile
POST /api/v1/users/me/deactivate → Deactivate account
```

---

## Access Cloud Database

### GUI Access (pgAdmin)
1. Visit: https://console.neon.tech
2. Username: `neondb_owner`
3. Database: `fuel4exam`

### Command Line (psql)
```bash
psql postgresql://neondb_owner:npg_I15hUKkEPGet@ep-lively-art-azfphgc0-pooler.c-3.ap-southeast-1.aws.neon.tech/fuel4exam?sslmode=require&channel_binding=require

# Check tables
\dt
# Check users
SELECT * FROM users;
```

---

## Project Structure (Simplified)

```
app/
├── core/              → Configuration & security
├── db/                → Database models
├── schemas/           → Request/response validation
├── services/          → Business logic
├── api/               → HTTP endpoints
└── exceptions/        → Error handling

main.py               → Application starter
seed.py               → Database seeder
```

---

## Common Commands

```bash
# Run with auto-reload (development)
python main.py

# Run without reload (production-like)
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run with specific workers (production)
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app

# Initialize database
python -c "from app.db.session import init_db; init_db()"

# Seed sample data
python seed.py

# Run with Docker
docker build -t fuel4exam .
docker run -p 8000:8000 fuel4exam

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

---

## Environment Variables

```bash
# Key variables in .env
DATABASE_URL=postgresql://...           # Database connection
SECRET_KEY=your-secret-key              # JWT signing key
DEBUG=False                             # Debug mode
ENVIRONMENT=production                  # Environment type
ALLOWED_ORIGINS=http://localhost:3000   # CORS origins
```

---

## Troubleshooting

### Issue: Database connection error
```
Solution: Check DATABASE_URL in .env
          Verify internet connectivity
          Check firewall/VPN settings
```

### Issue: Token validation fails
```
Solution: Ensure SECRET_KEY is correct
          Check token hasn't expired
          Use correct Authorization header format
```

### Issue: CORS errors in browser
```
Solution: Add your frontend URL to ALLOWED_ORIGINS in .env
          Example: http://localhost:3000
```

### Issue: Port 8000 already in use
```
Solution: python main.py --port 8001
          Or kill existing process: lsof -ti:8000 | xargs kill -9
```

---

## Next Steps

1. ✅ API is running and tested
2. 📖 Read [DEVELOPMENT.md](DEVELOPMENT.md) for development guide
3. 📚 Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for full API reference
4. 🏗️ Review [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for architecture
5. 🔨 Start building features!

---

## Key Features Implemented ✅

- ✅ User registration with email validation
- ✅ User login with JWT authentication
- ✅ Token refresh mechanism
- ✅ User profile management
- ✅ Password hashing with bcrypt
- ✅ Account activation/deactivation
- ✅ CORS support
- ✅ Comprehensive error handling
- ✅ Production-ready structure
- ✅ Docker deployment ready

---

## Production Deployment

### Using Docker Compose
```bash
# Start production environment
docker-compose up -d

# Check logs
docker-compose logs -f api

# Stop everything
docker-compose down
```

### Manual Deployment
```bash
# Install production ASGI server
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app

# Behind Nginx reverse proxy with SSL/TLS
```

---

## Support

- 📖 Documentation: See README.md, DEVELOPMENT.md, API_DOCUMENTATION.md
- 🐛 Issues: Check troubleshooting section
- 💬 Questions: Review inline code comments and docstrings

---

## What's Next?

The foundation is complete! You can now:

- 🧪 Build and test new features
- 🎓 Add exam functionality
- 🤖 Integrate LLM services
- 📊 Add analytics and reporting
- 🔐 Implement 2FA authentication
- 📧 Add email verification
- 💳 Add payment processing

Happy coding! 🚀
