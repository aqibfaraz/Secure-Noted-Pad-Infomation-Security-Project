# 🚀 Secure Notepad Application - RUNNING

## Server Status

### ✅ Backend Server
- **URL**: http://localhost:5000
- **Status**: Running (Flask Development Server)
- **Framework**: Flask 2.3.3
- **Features**:
  - REST API endpoints for authentication
  - Note CRUD operations
  - Maze-Card Hybrid Cipher encryption
  - JWT Token authentication

### ✅ Frontend Server  
- **URL**: http://localhost:3000
- **Status**: Running (Vite Development Server)
- **Framework**: React 18.2.0 + Tailwind CSS
- **Features**:
  - Login/Signup interface
  - Notepad with encryption/decryption
  - Responsive design
  - Real-time updates

### ⚠️ Database Server
- **Status**: **Requires Setup**
- **Type**: MySQL 5.7+
- **Setup Instructions**: See below

---

## 🎯 Next Steps

### 1. Set Up MySQL Database

**Important**: Before you can create or view notes, you must set up the MySQL database.

#### Option A: Using MySQL Command Line
```bash
# Open MySQL
mysql -u root -p

# Run the schema
source secure-notepad/database/schema.sql

# Verify
USE secure_notepad;
SHOW TABLES;
```

#### Option B: Using MySQL Workbench
1. Open MySQL Workbench
2. Create new connection (if needed)
3. File → Open SQL Script
4. Select: `secure-notepad/database/schema.sql`
5. Execute (lightning bolt icon)

#### Option C: Using Python Helper Script
```bash
# Run setup helper
python backend/setup_db.py
```

### 2. Update Backend Environment

Make sure `backend/.env` has correct MySQL credentials:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=secure_notepad
```

### 3. Open Application

**Once database is set up:**
1. Open your browser
2. Go to: **http://localhost:3000**
3. You should see the login page

---

## 📝 Test the Application

### 1. Create Account
- Click "Sign up here"
- Username: `testuser`
- Password: `password123`
- Click "Sign Up"

### 2. Login
- Username: `testuser`
- Password: `password123`
- Click "Login"

### 3. Create a Note
1. Enter Master Key: `mykey123`
2. Write note: "Hello Secure World!"
3. Click "Create Note"

### 4. View & Decrypt
1. Note appears in list (encrypted)
2. Click "Decrypt"
3. Enter Master Key: `mykey123`
4. See original content!

### 5. Edit Note
1. Click "Edit"
2. Modify text
3. Click "Save"

### 6. Delete Note
1. Click "Delete"
2. Confirm deletion

---

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/signup` - Register
- `POST /api/auth/login` - Login

### Notes
- `GET /api/notes` - Get all notes
- `POST /api/notes` - Create note
- `POST /api/notes/<id>/decrypt` - Decrypt note
- `PUT /api/notes/<id>` - Update note
- `DELETE /api/notes/<id>` - Delete note

**See docs/API.md for full documentation**

---

## 🛑 Troubleshooting

### Issue: "Cannot connect to database"
**Solution**: Set up MySQL database (see above)

### Issue: "Port 5000 already in use"
**Solution**: 
```bash
# Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue: "Port 3000 already in use"
**Solution**:
```bash
# Find and kill process
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Issue: Frontend shows errors
**Solution**: 
```bash
# In frontend directory
rm -r node_modules package-lock.json
npm install
npm run dev
```

### Issue: "Module not found"
**Solution**: Make sure all dependencies installed
```bash
# Backend
cd backend && pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

---

## 📊 Terminal Windows

You should have **2 terminal windows** open:

1. **Terminal 1 (Backend)**
   ```
   Python virtual environment active
   Flask running on http://localhost:5000
   Shows "Running on..." message
   ```

2. **Terminal 2 (Frontend)**
   ```
   Node.js environment
   Vite running on http://localhost:3000
   Shows "Local: http://localhost:3000"
   ```

---

## 🔒 Security Notes

- Master key is **never stored** on server
- Passwords are hashed using PBKDF2
- Notes encrypted with custom Maze-Card cipher
- JWT tokens expire after 24 hours
- All API calls require authentication

---

## 📚 Documentation

- [README.md](README.md) - Project overview
- [SETUP.md](SETUP.md) - Detailed setup instructions
- [docs/API.md](docs/API.md) - API documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contributing guidelines

---

## ✨ Ready to Go!

**Everything is set up and running!**

1. **Set up your MySQL database** (critical!)
2. **Open http://localhost:3000**
3. **Create an account and start encrypting notes**

Enjoy your secure notepad! 🎉

---

**Last Updated**: January 7, 2026
**Version**: 1.0.0
