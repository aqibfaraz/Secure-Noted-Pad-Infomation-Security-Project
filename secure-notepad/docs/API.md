# Secure Notepad API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
All endpoints (except `/auth/signup` and `/auth/login`) require a JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## Endpoints

### 1. Authentication Endpoints

#### Sign Up
Create a new user account.

**Endpoint**: `POST /auth/signup`

**Request Body**:
```json
{
  "username": "string (3-100 characters)",
  "password": "string (6+ characters)"
}
```

**Response** (201 Created):
```json
{
  "message": "User created successfully"
}
```

**Error Responses**:
- 400: "Username and password are required"
- 400: "Username must be between 3 and 100 characters"
- 400: "Password must be at least 6 characters"
- 409: "Username already exists"

---

#### Login
Authenticate user and receive JWT token.

**Endpoint**: `POST /auth/login`

**Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```

**Response** (200 OK):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user_id": 1,
  "username": "john_doe"
}
```

**Error Responses**:
- 400: "Username and password are required"
- 401: "Invalid username or password"

---

### 2. Note Endpoints

#### Get All Notes
Retrieve all notes for the authenticated user.

**Endpoint**: `GET /notes`

**Headers**:
```
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "cipher_text": "10♠ 3♥ 8♣ 8♦ 9♠ ...",
    "created_at": "2024-01-07 10:30:00"
  },
  {
    "id": 2,
    "cipher_text": "5♣ 7♠ 2♥ 4♦ ...",
    "created_at": "2024-01-07 09:15:00"
  }
]
```

**Error Responses**:
- 401: "Token is missing" or "Token is invalid"

---

#### Create Note
Create a new encrypted note.

**Endpoint**: `POST /notes`

**Headers**:
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "content": "string (1-10000 characters)",
  "master_key": "string"
}
```

**Response** (201 Created):
```json
{
  "message": "Note created successfully",
  "note_id": 1
}
```

**Error Responses**:
- 400: "Content and master_key are required"
- 400: "Note content cannot be empty"
- 400: "Note content cannot exceed 10000 characters"
- 401: "Token is missing" or "Token is invalid"

**Notes**:
- Master key is used for encryption but never stored
- Same master key required for decryption
- Content is automatically encrypted before storage

---

#### Decrypt Note
Decrypt a specific note using master key.

**Endpoint**: `POST /notes/<note_id>/decrypt`

**Headers**:
```
Authorization: Bearer <token>
Content-Type: application/json
```

**URL Parameters**:
- `note_id` (integer): The ID of the note to decrypt

**Request Body**:
```json
{
  "master_key": "string"
}
```

**Response** (200 OK):
```json
{
  "content": "This is the original note content",
  "note_id": 1
}
```

**Error Responses**:
- 400: "master_key is required"
- 404: "Note not found"
- 401: "Token is missing" or "Token is invalid"
- 500: "Error decrypting note" (usually means wrong master key)

---

#### Update Note
Update (re-encrypt) a note with new content.

**Endpoint**: `PUT /notes/<note_id>`

**Headers**:
```
Authorization: Bearer <token>
Content-Type: application/json
```

**URL Parameters**:
- `note_id` (integer): The ID of the note to update

**Request Body**:
```json
{
  "content": "string (1-10000 characters)",
  "master_key": "string"
}
```

**Response** (200 OK):
```json
{
  "message": "Note updated successfully"
}
```

**Error Responses**:
- 400: "Content and master_key are required"
- 400: "Note content cannot be empty"
- 400: "Note content cannot exceed 10000 characters"
- 404: "Note not found"
- 401: "Token is missing" or "Token is invalid"

**Notes**:
- Original content is decrypted, then re-encrypted with new content
- Master key must match original encryption key

---

#### Delete Note
Delete a specific note permanently.

**Endpoint**: `DELETE /notes/<note_id>`

**Headers**:
```
Authorization: Bearer <token>
```

**URL Parameters**:
- `note_id` (integer): The ID of the note to delete

**Response** (200 OK):
```json
{
  "message": "Note deleted successfully"
}
```

**Error Responses**:
- 404: "Note not found"
- 401: "Token is missing" or "Token is invalid"

---

### 3. Utility Endpoints

#### Health Check
Check if API is running.

**Endpoint**: `GET /health`

**Response** (200 OK):
```json
{
  "status": "ok"
}
```

---

## Error Handling

All errors follow this format:
```json
{
  "message": "Error description"
}
```

**Common HTTP Status Codes**:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 409: Conflict
- 500: Server Error

---

## Request/Response Examples

### Example 1: Complete Flow

**1. Sign Up**
```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "password": "secure123"}'
```

**2. Login**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "password": "secure123"}'
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": 1,
  "username": "john_doe"
}
```

**3. Create Note**
```bash
curl -X POST http://localhost:5000/api/notes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{"content": "My secret note", "master_key": "mykey123"}'
```

**4. Get Notes**
```bash
curl -X GET http://localhost:5000/api/notes \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**5. Decrypt Note**
```bash
curl -X POST http://localhost:5000/api/notes/1/decrypt \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{"master_key": "mykey123"}'
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production:
- Consider implementing Flask-Limiter
- Recommended: 100 requests per minute per IP

## CORS

CORS is enabled for all origins. For production, restrict to specific domains:
```python
CORS(app, resources={r"/api/*": {"origins": ["https://yourdomain.com"]}})
```

## API Version

Current API Version: 1.0.0

---

**Last Updated**: January 2026
