# Fuel4Exam API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## Health Check

### Get Server Health
```http
GET /health
```

**Response 200 OK:**
```json
{
  "status": "healthy",
  "service": "Fuel4Exam",
  "version": "1.0.0",
  "environment": "production"
}
```

---

## Authentication Endpoints

### 1. Register User

**Endpoint:** `POST /auth/register`

**Description:** Create a new user account

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Validation Rules:**
- `email`: Valid email format, must be unique
- `username`: 3-50 chars, alphanumeric with `-` or `_`, must be unique
- `password`: Minimum 8 characters
- `first_name`: 1-100 characters
- `last_name`: 1-100 characters

**Response 201 Created:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "role": "student",
    "status": "active",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Error Response 409 Conflict:**
```json
{
  "error": "UserAlreadyExistsException",
  "detail": "Email user@example.com already registered",
  "status_code": 409
}
```

**Error Response 422 Unprocessable Entity:**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "username"],
      "msg": "Username must be alphanumeric with underscores or hyphens",
      "input": "john@doe"
    }
  ]
}
```

---

### 2. Login User

**Endpoint:** `POST /auth/login`

**Description:** Authenticate user and get tokens

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}
```

**Response 200 OK:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "role": "student",
    "status": "active",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Error Response 401 Unauthorized:**
```json
{
  "error": "InvalidCredentialsException",
  "detail": "Invalid email or password",
  "status_code": 401
}
```

---

### 3. Refresh Access Token

**Endpoint:** `POST /auth/refresh`

**Description:** Get a new access token using refresh token

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response 200 OK:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 30
}
```

**Error Response 401 Unauthorized:**
```json
{
  "error": "InvalidTokenException",
  "detail": "Invalid or expired token",
  "status_code": 401
}
```

---

## User Profile Endpoints

### 4. Get Current User Profile

**Endpoint:** `GET /users/me`

**Description:** Get the current authenticated user's profile

**Authorization:** Required ✓

**Response 200 OK:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Software developer interested in AI",
  "profile_picture_url": "https://cdn.example.com/profiles/1.jpg",
  "phone_number": "+1-555-0123",
  "role": "student",
  "status": "active",
  "is_email_verified": true,
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-16T14:45:30Z",
  "last_login_at": "2024-01-16T14:45:30Z"
}
```

**Error Response 401 Unauthorized:**
```json
{
  "detail": "Invalid or expired token"
}
```

---

### 5. Get User Profile by ID

**Endpoint:** `GET /users/{user_id}`

**Description:** Get another user's profile (public endpoint)

**Parameters:**
- `user_id` (path, required): User ID to retrieve

**Response 200 OK:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Software developer interested in AI",
  "profile_picture_url": "https://cdn.example.com/profiles/1.jpg",
  "phone_number": "+1-555-0123",
  "role": "student",
  "status": "active",
  "is_email_verified": true,
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-16T14:45:30Z",
  "last_login_at": "2024-01-16T14:45:30Z"
}
```

**Error Response 404 Not Found:**
```json
{
  "error": "UserNotFoundException",
  "detail": "User with ID 999 not found",
  "status_code": 404
}
```

---

### 6. Update Current User Profile

**Endpoint:** `PUT /users/me`

**Description:** Update current user's profile information

**Authorization:** Required ✓

**Request Body (all fields optional):**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "bio": "Updated bio",
  "profile_picture_url": "https://cdn.example.com/new-profile.jpg",
  "phone_number": "+1-555-0456"
}
```

**Validation Rules:**
- `first_name`: 1-100 chars (optional)
- `last_name`: 1-100 chars (optional)
- `bio`: max 500 chars (optional)
- `profile_picture_url`: valid URL (optional)
- `phone_number`: max 20 chars (optional)

**Response 200 OK:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "first_name": "Jane",
  "last_name": "Smith",
  "bio": "Updated bio",
  "profile_picture_url": "https://cdn.example.com/new-profile.jpg",
  "phone_number": "+1-555-0456",
  "role": "student",
  "status": "active",
  "is_email_verified": true,
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-17T16:20:15Z",
  "last_login_at": "2024-01-16T14:45:30Z"
}
```

**Error Response 401 Unauthorized:**
```json
{
  "detail": "Missing authorization header"
}
```

---

### 7. Deactivate User Account

**Endpoint:** `POST /users/me/deactivate`

**Description:** Deactivate current user's account

**Authorization:** Required ✓

**Request Body:** (empty)

**Response 200 OK:**
```json
{
  "message": "Account deactivated successfully",
  "success": true
}
```

**Error Response 401 Unauthorized:**
```json
{
  "detail": "Invalid or expired token"
}
```

---

## Error Response Format

All error responses follow this standard format:

```json
{
  "error": "ErrorType",
  "detail": "Detailed error message",
  "status_code": 400
}
```

### HTTP Status Codes

| Code | Meaning | Common Cause |
|------|---------|--------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource already exists |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

---

## Token Format

Tokens are JWT (JSON Web Tokens) with the following structure:

**Header:**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload:**
```json
{
  "sub": "1",
  "exp": 1705430400,
  "iat": 1705426800
}
```

**Token Expiration:**
- Access Token: 30 minutes
- Refresh Token: 7 days

---

## Rate Limiting

Currently no rate limiting is implemented. In production, implement rate limiting based on:
- IP address: 1000 requests/hour
- User ID: 5000 requests/hour

---

## CORS Headers

The API supports CORS with the following configured origins:
```
http://localhost:3000
http://localhost:8000
http://localhost:5173
```

---

## Example Workflow

### Complete User Journey

1. **Register New User**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{
       "email": "newuser@example.com",
       "username": "newuser",
       "password": "SecurePass123",
       "first_name": "John",
       "last_name": "Doe"
     }'
   ```

2. **Login User**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{
       "email": "newuser@example.com",
       "password": "SecurePass123"
     }'
   ```

3. **Use Access Token**
   ```bash
   curl -X GET http://localhost:8000/api/v1/users/me \
     -H "Authorization: Bearer <access_token>"
   ```

4. **Update Profile**
   ```bash
   curl -X PUT http://localhost:8000/api/v1/users/me \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "bio": "Updated bio"
     }'
   ```

5. **Refresh Token**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/refresh \
     -H "Content-Type: application/json" \
     -d '{
       "refresh_token": "<refresh_token>"
     }'
   ```

---

## User Roles

The system supports three user roles:

| Role | Description | Permissions |
|------|-------------|-------------|
| `candidate` | Exam preparation candidate | Take exams, view results |

---

## User Status

Users can have the following statuses:

| Status | Description |
|--------|-------------|
| `active` | User account is active |
| `inactive` | User account is inactive |
| `suspended` | User account is suspended |

---

## Testing the API

### Using cURL

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d @register.json

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d @login.json
```

### Using Postman

1. Import the OpenAPI schema from: `http://localhost:8000/api/openapi.json`
2. Set base URL to: `http://localhost:8000/api/v1`
3. Use the "Authorization" tab to add Bearer token
4. Test endpoints from the collection

### Using Python Requests

```python
import requests

# Register
response = requests.post(
    'http://localhost:8000/api/v1/auth/register',
    json={
        'email': 'user@example.com',
        'username': 'username',
        'password': 'Password123',
        'first_name': 'John',
        'last_name': 'Doe'
    }
)
data = response.json()
access_token = data['access_token']

# Get profile
response = requests.get(
    'http://localhost:8000/api/v1/users/me',
    headers={'Authorization': f'Bearer {access_token}'}
)
print(response.json())
```

---

## API Documentation UI

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI Schema**: http://localhost:8000/api/openapi.json

---

## Support

For API issues or questions, refer to the development guide or contact support.
