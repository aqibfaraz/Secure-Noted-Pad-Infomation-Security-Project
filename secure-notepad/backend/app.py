"""
Secure Notepad Application - Flask Backend
Handles authentication, note management, and encryption/decryption
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import sqlite3
import os
from functools import wraps
from cipher import MazeCardCipher

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_EXPIRATION'] = 86400  # 24 hours

# SQLite Database Configuration
# Use project-root database file so frontend/backend share the same DB
DB_PATH = os.getenv(
    'DB_PATH',
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'secure_notepad.db'))
)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})


def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def token_required(f):
    """Decorator for routes requiring authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated


# ==================== AUTHENTICATION ENDPOINTS ====================

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """
    User signup endpoint.
    
    Request body:
    {
        "username": "string",
        "password": "string"
    }
    """
    data = request.get_json()
    
    # Validation
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400
    
    username = data['username'].strip()
    password = data['password']
    
    # Validate username length
    if len(username) < 3 or len(username) > 100:
        return jsonify({'message': 'Username must be between 3 and 100 characters'}), 400
    
    # Validate password strength
    if len(password) < 6:
        return jsonify({'message': 'Password must be at least 6 characters'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            return jsonify({'message': 'Username already exists'}), 409
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        # Insert new user
        cursor.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (username, password_hash)
        )
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'User created successfully'}), 201
    
    except Exception as e:
        return jsonify({'message': f'Error creating user: {str(e)}'}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    User login endpoint.
    
    Request body:
    {
        "username": "string",
        "password": "string"
    }
    
    Response:
    {
        "token": "JWT_TOKEN",
        "user_id": "int",
        "username": "string"
    }
    """
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400
    
    username = data['username']
    password = data['password']
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, username, password_hash FROM users WHERE username = ?',
            (username,)
        )
        user = cursor.fetchone()
        conn.close()
        
        if not user or not check_password_hash(user['password_hash'], password):
            return jsonify({'message': 'Invalid username or password'}), 401
        
        # Generate JWT token
        token = jwt.encode(
            {
                'user_id': user['id'],
                'username': user['username'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=app.config['JWT_EXPIRATION'])
            },
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        
        return jsonify({
            'token': token,
            'user_id': user['id'],
            'username': user['username']
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Error logging in: {str(e)}'}), 500


# ==================== NOTE ENDPOINTS ====================

@app.route('/api/notes', methods=['GET'])
@token_required
def get_notes(user_id):
    """Get all notes for the authenticated user."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, cipher_text, created_at FROM notes WHERE user_id = ? ORDER BY created_at DESC',
            (user_id,)
        )
        notes = cursor.fetchall()
        conn.close()
        
        return jsonify([dict(note) for note in notes]), 200
    
    except Exception as e:
        return jsonify({'message': f'Error retrieving notes: {str(e)}'}), 500


@app.route('/api/notes', methods=['POST'])
@token_required
def create_note(user_id):
    """
    Create a new encrypted note.
    
    Request body:
    {
        "content": "string",
        "master_key": "string"
    }
    """
    data = request.get_json()
    
    if not data or not data.get('content') or not data.get('master_key'):
        return jsonify({'message': 'Content and master_key are required'}), 400
    
    content = data['content']
    master_key = data['master_key']
    
    # Validate
    if len(content) == 0:
        return jsonify({'message': 'Note content cannot be empty'}), 400
    
    if len(content) > 10000:
        return jsonify({'message': 'Note content cannot exceed 10000 characters'}), 400
    
    try:
        # Encrypt content
        cipher_text = MazeCardCipher.encrypt(content, master_key)
        
        # Save to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO notes (user_id, cipher_text) VALUES (?, ?)',
            (user_id, cipher_text)
        )
        conn.commit()
        note_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'message': 'Note created successfully',
            'note_id': note_id
        }), 201
    
    except Exception as e:
        return jsonify({'message': f'Error creating note: {str(e)}'}), 500


@app.route('/api/notes/<int:note_id>/decrypt', methods=['POST'])
@token_required
def decrypt_note(user_id, note_id):
    """
    Decrypt a note.
    
    Request body:
    {
        "master_key": "string"
    }
    """
    data = request.get_json()
    
    if not data or not data.get('master_key'):
        return jsonify({'message': 'master_key is required'}), 400
    
    master_key = data['master_key']
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Verify ownership
        cursor.execute(
            'SELECT cipher_text FROM notes WHERE id = ? AND user_id = ?',
            (note_id, user_id)
        )
        note = cursor.fetchone()
        conn.close()
        
        if not note:
            return jsonify({'message': 'Note not found'}), 404
        
        # Decrypt
        plaintext = MazeCardCipher.decrypt(note['cipher_text'], master_key)
        
        return jsonify({
            'content': plaintext,
            'note_id': note_id
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Error decrypting note: {str(e)}'}), 500


@app.route('/api/notes/<int:note_id>', methods=['PUT'])
@token_required
def update_note(user_id, note_id):
    """
    Update a note (re-encrypt with new content).
    
    Request body:
    {
        "content": "string",
        "master_key": "string"
    }
    """
    data = request.get_json()
    
    if not data or not data.get('content') or not data.get('master_key'):
        return jsonify({'message': 'Content and master_key are required'}), 400
    
    content = data['content']
    master_key = data['master_key']
    
    # Validate
    if len(content) == 0:
        return jsonify({'message': 'Note content cannot be empty'}), 400
    
    if len(content) > 10000:
        return jsonify({'message': 'Note content cannot exceed 10000 characters'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Verify ownership
        cursor.execute(
            'SELECT id FROM notes WHERE id = ? AND user_id = ?',
            (note_id, user_id)
        )
        if not cursor.fetchone():
            return jsonify({'message': 'Note not found'}), 404
        
        # Encrypt new content
        cipher_text = MazeCardCipher.encrypt(content, master_key)
        
        # Update note
        cursor.execute(
            'UPDATE notes SET cipher_text = ? WHERE id = ?',
            (cipher_text, note_id)
        )
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Note updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'message': f'Error updating note: {str(e)}'}), 500


@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
@token_required
def delete_note(user_id, note_id):
    """Delete a note."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Verify ownership
        cursor.execute(
            'SELECT id FROM notes WHERE id = ? AND user_id = ?',
            (note_id, user_id)
        )
        if not cursor.fetchone():
            return jsonify({'message': 'Note not found'}), 404
        
        # Delete note
        cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Note deleted successfully'}), 200
    
    except Exception as e:
        return jsonify({'message': f'Error deleting note: {str(e)}'}), 500


# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok'}), 200


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'message': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({'message': 'Internal server error'}), 500


if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=5000)
