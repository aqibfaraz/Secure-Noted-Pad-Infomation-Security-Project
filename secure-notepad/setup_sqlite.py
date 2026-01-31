"""
Secure Notepad - SQLite Setup
Converts the app to use SQLite instead of MySQL
No installation needed - works out of the box!
"""

import sqlite3
import os

DB_PATH = "secure_notepad.db"

def setup_sqlite_database():
    """Create SQLite database and tables"""
    try:
        # Remove old database if exists
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            print(f"Removed old database")
        
        # Create connection
        print("Creating SQLite database...")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create users table
        print("Creating 'users' table...")
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create notes table
        print("Creating 'notes' table...")
        cursor.execute("""
            CREATE TABLE notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                cipher_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Create indices
        print("Creating indices...")
        cursor.execute("CREATE INDEX idx_username ON users(username)")
        cursor.execute("CREATE INDEX idx_user_id ON notes(user_id)")
        cursor.execute("CREATE INDEX idx_created_at ON notes(created_at)")
        
        # Commit
        conn.commit()
        conn.close()
        
        print("\n" + "="*50)
        print("✅ SQLITE DATABASE SETUP SUCCESSFUL!")
        print("="*50)
        print(f"Database: {DB_PATH}")
        print("Tables: users, notes")
        print("\nYou can now use the Secure Notepad application!")
        print("No MySQL installation needed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*50)
    print("SECURE NOTEPAD - SQLITE SETUP")
    print("="*50 + "\n")
    
    setup_sqlite_database()
