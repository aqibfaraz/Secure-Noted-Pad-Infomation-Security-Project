"""
Database Setup Script for Secure Notepad
Creates the database and tables if they don't exist
"""

import pymysql
import sys

# Database connection parameters
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''  # Change if you have a password
DB_NAME = 'secure_notepad'

def setup_database():
    """Create database and tables"""
    try:
        # Connect to MySQL without selecting a database
        print("Connecting to MySQL...")
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            charset='utf8mb4'
        )
        
        print("✓ Connected to MySQL")
        cursor = conn.cursor()
        
        # Create database
        print(f"Creating database '{DB_NAME}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"✓ Database created/exists")
        
        # Select database
        cursor.execute(f"USE {DB_NAME}")
        
        # Create users table
        print("Creating 'users' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Users table created/exists")
        
        # Create notes table
        print("Creating 'notes' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                cipher_text LONGTEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_user_id (user_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Notes table created/exists")
        
        # Create indices
        print("Creating indices...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_username ON users(username)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON notes(created_at)")
        print("✓ Indices created/exist")
        
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n" + "="*50)
        print("✅ DATABASE SETUP SUCCESSFUL!")
        print("="*50)
        print(f"Database: {DB_NAME}")
        print("Tables: users, notes")
        print("\nYou can now use the Secure Notepad application!")
        return True
        
    except pymysql.Error as e:
        print(f"\n❌ MySQL Error: {e}")
        print("\nPossible issues:")
        print("1. MySQL is not installed or not running")
        print("2. Wrong username/password")
        print("3. MySQL not accessible on localhost:3306")
        print("\nSolutions:")
        print("- Install MySQL from https://dev.mysql.com/downloads/mysql/")
        print("- Start MySQL service: services.msc → MySQL → Start")
        print("- Or use XAMPP/WAMP which includes MySQL")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*50)
    print("SECURE NOTEPAD - DATABASE SETUP")
    print("="*50 + "\n")
    
    success = setup_database()
    sys.exit(0 if success else 1)
