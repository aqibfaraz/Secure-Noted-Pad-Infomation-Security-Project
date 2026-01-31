-- Sample test data (for development only - do not use in production)
-- Note: Passwords must be hashed using the same method as the application

INSERT INTO users (username, password_hash) VALUES
('testuser', 'pbkdf2:sha256:600000$XYZ$ABC...');  -- This is a placeholder - use actual hashed passwords

-- You can generate proper password hashes using Python:
-- from werkzeug.security import generate_password_hash
-- password_hash = generate_password_hash('your-password')
