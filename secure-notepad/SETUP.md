# Secure Notepad - Setup Instructions

## Quick Start Guide

### System Requirements
- **Node.js**: 16.0.0 or higher
- **Python**: 3.8 or higher
- **MySQL**: 5.7 or higher
- **npm**: 7.0.0 or higher
- **git**: Latest version

### Step 1: Clone/Download Project
```bash
cd "c:\Users\sk\OneDrive\Desktop\Infomation security"
# Project is already in secure-notepad folder
```

### Step 2: Set Up MySQL Database

**Option A: Using MySQL Command Line**
```bash
# Login to MySQL
mysql -u root -p

# Run schema
source secure-notepad/database/schema.sql
```

**Option B: Using MySQL Workbench**
1. Open MySQL Workbench
2. File → Open SQL Script → Select `database/schema.sql`
3. Execute the script

Verify database creation:
```sql
USE secure_notepad;
SHOW TABLES;
```

### Step 3: Set Up Backend

```bash
# Navigate to backend
cd backend

# Create .env file
copy .env.example .env

# Edit .env with your MySQL password
# Open .env and update:
# DB_PASSWORD=your_mysql_password
# SECRET_KEY=generate_random_string

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Or on macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test the backend
python -c "from cipher import MazeCardCipher; print('Cipher OK')"

# Start Flask server
python app.py
```

**Expected Output**:
```
 * Serving Flask app 'app'
 * Running on http://0.0.0.0:5000
```

### Step 4: Set Up Frontend (New Terminal)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Expected Output**:
```
VITE v4.x.x  ready in xxx ms

➜  Local:   http://localhost:3000/
```

### Step 5: Open Application

Open your browser and go to:
```
http://localhost:3000
```

You should see the login page.

---

## Testing the Application

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
- Enter Master Key: `mymaster123`
- Write a note: "This is my first secure note!"
- Click "Create Note"

### 4. View Encrypted Note
- You should see your note in the list (showing encrypted text)

### 5. Decrypt Note
- Click "Decrypt"
- Your original note appears!

### 6. Edit Note
- Click "Edit"
- Modify the text
- Click "Save"

### 7. Delete Note
- Click "Delete"
- Confirm deletion

---

## Troubleshooting

### Backend Issues

**Error: "No module named 'flask'"**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate
pip install -r requirements.txt
```

**Error: "Can't connect to MySQL server"**
- Verify MySQL is running
- Check DB_HOST and DB_PASSWORD in .env
- Default: localhost, root, (no password)

**Error: "Access denied for user 'root'@'localhost'"**
- Update DB_PASSWORD in .env
- Verify MySQL password is correct

**Port 5000 already in use**
```bash
# Change port in app.py:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Frontend Issues

**Error: "npm: command not found"**
- Install Node.js from nodejs.org
- Restart terminal after installation

**Error: "Cannot find module"**
```bash
# Clean install
rm -r node_modules
rm package-lock.json
npm install
```

**Port 3000 already in use**
```bash
# Kill process on Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or change port in vite.config.js
```

### Database Issues

**Error: "Unknown database 'secure_notepad'"**
```bash
mysql -u root -p < database/schema.sql
```

**Error: "Access denied for user 'root'@'localhost'"**
- Verify MySQL password
- Update .env file

---

## Project Architecture

```
Frontend (React)           Backend (Flask)            Database (MySQL)
    ↓                          ↓                           ↓
Client UI    ← Axios →    REST API         ← PyMySQL →  Tables
- Login                   - Authentication              - users
- Notepad                 - Note CRUD                   - notes
- Encryption              - Cipher Logic

Flow: User → React UI → Flask API → MySQL DB → Response back
```

---

## Key Features Walkthrough

### 1. Master Key Security
- Master key is **never stored** on server
- Required for every encryption/decryption
- Losing master key = losing access to notes
- **Recommendation**: Remember your master key!

### 2. Encryption Process
```
Plaintext: "Hello"
Master Key: "secret123"
↓
Character Mapping: A→10♠, B→3♥, ...
↓
Multi-round Shuffling (2-4 rounds)
↓
Ciphertext: "10♠ 3♥ 8♣ 8♦ ..."
↓
Stored in Database
```

### 3. Decryption Process
```
Ciphertext: "10♠ 3♥ 8♣ 8♦ ..."
Master Key: "secret123" (MUST match)
↓
Reverse Shuffling (4-2 rounds)
↓
Symbol to Character Mapping
↓
Plaintext: "Hello"
↓
Displayed to User
```

---

## Security Best Practices

✅ **Do This**
- Use strong master keys (10+ characters)
- Remember your master key
- Use HTTPS in production
- Keep dependencies updated
- Regular backups of database

❌ **Don't Do This**
- Share your master key
- Write master key in code
- Use simple passwords
- Run without HTTPS in production
- Expose SECRET_KEY on client

---

## Running with Docker (Optional)

```bash
# Install Docker Desktop

# Build and run
docker-compose up --build

# Access at http://localhost:3000
```

---

## Stopping the Application

**Backend**:
- Press `Ctrl + C` in backend terminal

**Frontend**:
- Press `Ctrl + C` in frontend terminal

**Database**:
- Keep MySQL running or stop via Services

---

## Production Deployment

Before deploying to production:

1. **Change all secrets**
   ```bash
   # Generate strong SECRET_KEY
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Update CORS**
   ```python
   # In app.py
   CORS(app, resources={r"/api/*": {"origins": ["https://yourdomain.com"]}})
   ```

3. **Use HTTPS**
   - Get SSL certificate (Let's Encrypt)
   - Configure reverse proxy (Nginx/Apache)

4. **Use Production Server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 app:app
   ```

5. **Update Database**
   - Use strong root password
   - Restrict MySQL access
   - Regular backups

---

## Next Steps

After confirming the app works:
1. Read [API Documentation](../docs/API.md)
2. Explore the source code
3. Customize UI/Branding
4. Add features
5. Deploy to production

---

## Support Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Vite Documentation](https://vitejs.dev/)

---

**Questions?** Check the README.md for more information.
