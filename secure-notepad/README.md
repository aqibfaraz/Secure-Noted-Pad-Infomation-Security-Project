# Secure Notepad

Full-stack notes app with client-controlled encryption. The frontend (React) sends only ciphertext to the backend (Flask), which stores it in SQLite (default) or MySQL (optional). A custom Maze-Card multi-round cipher maps characters to playing-card symbols and performs deterministic shuffles seeded by the user master key.

## What You Get
- End-to-end note encryption with a master key that is never stored or transmitted beyond each request
- JWT auth with PBKDF2 password hashing
- CRUD for encrypted notes (create, read metadata, decrypt, update, delete)
- React + Tailwind UI with login/signup and a notepad dashboard
- Ready-to-run SQLite setup; MySQL schema provided for alternative deployment

## Architecture
- **Frontend** (React, Vite, Tailwind): pages in [frontend/src](frontend/src) call the API via [frontend/src/utils/api.js](frontend/src/utils/api.js).
- **Backend** (Flask): routes in [backend/app.py](backend/app.py) handle auth, note CRUD, and cipher calls.
- **Cipher**: custom symmetric algorithm in [backend/cipher.py](backend/cipher.py).
- **Database**: SQLite file `secure_notepad.db` by default (created by [setup_sqlite.py](setup_sqlite.py)); optional MySQL schema in [database/schema.sql](database/schema.sql).
- **Docs**: endpoint details in [docs/API.md](docs/API.md).

## Data and Encryption Workflow
1. User signs up/logs in → receives JWT.
2. User enters a **master key** locally in the UI (never persisted client-side beyond memory/localStorage entry, never stored server-side).
3. On create/update: frontend sends plaintext + master key to `/api/notes` → backend encrypts with `MazeCardCipher.encrypt` → only ciphertext is stored.
4. On decrypt: frontend sends master key to `/api/notes/<id>/decrypt` → backend verifies ownership and decrypts with the same master key → plaintext returned to the client.
5. JWT guards all note routes; tokens expire after 24 hours.

## Maze-Card Cipher (High Level)
- **Character mapping**: each supported char maps to a card rank/suit symbol (e.g., `A♠`, `10♥`).
- **Key-derived params**: from ASCII sum of the master key → seed, 2–4 shuffle rounds, suit order seed.
- **Encryption**: substitute chars → deterministic shuffle per round using the derived seed → join as space-separated card symbols.
- **Decryption**: recreate the same shuffle order in reverse → map cards back to chars. Wrong master key yields wrong plaintext, so the API returns an error if decryption fails.

## File Layout
```
backend/      Flask API, cipher
frontend/     React app (Vite + Tailwind)
database/     MySQL schema (optional)
docs/         API reference
setup_sqlite.py  SQLite bootstrapper (default)
```

## Quickstart (SQLite, recommended)
Prereqs: Python 3.8+, Node 16+, npm.

1) Create the SQLite DB
```bash
python setup_sqlite.py
```

2) Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt
set SECRET_KEY=change-me   # or put in .env
python app.py
```
Backend runs on http://localhost:5000.

3) Frontend (new terminal)
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on http://localhost:3000.

## Optional: MySQL Setup
If you prefer MySQL over SQLite:
```bash
mysql -u root -p < database/schema.sql
```
In [backend/app.py](backend/app.py), set `DB_PATH` to a MySQL connector or adapt the code (defaults to SQLite). Keep using the provided schema for table shape.

## Configuration
- `SECRET_KEY` (required): JWT signing key.
- `JWT_EXPIRATION` (optional): seconds, defaults to 86400 (24h).
- `DB_PATH` (optional): SQLite file path; defaults to project-root `secure_notepad.db`.
- Frontend base URL: set `VITE_API_URL` if the API is not on the same origin.

## API Surface
- Auth: `POST /api/auth/signup`, `POST /api/auth/login`.
- Notes: `GET /api/notes`, `POST /api/notes`, `POST /api/notes/<id>/decrypt`, `PUT /api/notes/<id>`, `DELETE /api/notes/<id>`.
See [docs/API.md](docs/API.md) for payloads and examples.

## How to Use (happy path)
1. Sign up, then log in (JWT stored in localStorage).
2. Enter your master key in the Notepad screen (it is required for every note action).
3. Create a note → ciphertext appears in your list.
4. Decrypt a note → plaintext shows temporarily in the UI; you can edit and save (re-encrypts).
5. Delete when needed; logout clears the token.

## Security Notes
- Master key is never stored server-side; losing it means losing access to your data.
- Passwords are hashed (PBKDF2) and tokens expire in 24h.
- Use HTTPS and a strong `SECRET_KEY` in production.
- Restrict CORS origins in production (see CORS config in [backend/app.py](backend/app.py)).

## Docker (optional)
```bash
docker-compose up --build
```

## Troubleshooting
- Wrong master key → decryption fails; try again with the exact key you encrypted with.
- Token issues → clear localStorage and log in again.
- Port conflicts → change Flask port in [backend/app.py](backend/app.py) and Vite port in `vite.config.js`.

## Credits
Built with React, Tailwind, Flask, SQLite/MySQL, and JWT.
