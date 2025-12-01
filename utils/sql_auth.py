# utils/sql_auth.py
import sqlite3
from pathlib import Path
import hashlib
import secrets
import time

# -----------------------------
# Database location
# -----------------------------
DB_PATH = Path("users.db")

def _get_conn():
    """Create SQLite connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------
# Initialize DB if not exists
# -----------------------------
def init_db():
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        full_name TEXT,
        salt TEXT,
        pwd_hash TEXT,
        created_at INTEGER
    );
    """)
    conn.commit()
    conn.close()

# -----------------------------
# Password hashing helpers
# -----------------------------
def hash_password(password: str, salt: str):
    """Returns salted SHA256 hash (simple & safe for demo; use bcrypt for production)."""
    h = hashlib.sha256()
    h.update((salt + password).encode("utf-8"))
    return h.hexdigest()

# -----------------------------
# Register user
# -----------------------------
def register_user(email: str, password: str, full_name: str = ""):
    """Create a new user if not already exists."""
    email = email.strip().lower()
    if not email or not password:
        return False, "Email and password required."

    init_db()
    conn = _get_conn()
    cur = conn.cursor()

    # Check if user already exists
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    if cur.fetchone():
        conn.close()
        return False, "User already exists."

    # Generate salt & hash password
    salt = secrets.token_hex(8)
    pwd_hash = hash_password(password, salt)

    # Insert new user
    cur.execute(
        "INSERT INTO users (email, full_name, salt, pwd_hash, created_at) VALUES (?, ?, ?, ?, ?)",
        (email, full_name, salt, pwd_hash, int(time.time())),
    )
    conn.commit()
    conn.close()

    return True, "Registration successful."

# -----------------------------
# Authenticate user
# -----------------------------
def authenticate_user(email: str, password: str):
    """Verify credentials and return user info if valid."""
    email = email.strip().lower()
    init_db()
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return False, "No such user."

    # Validate password
    expected_hash = row["pwd_hash"]
    computed_hash = hash_password(password, row["salt"])
    if computed_hash == expected_hash:
        user_info = {"email": row["email"], "full_name": row["full_name"]}
        return True, user_info
    else:
        return False, "Invalid credentials."

# -----------------------------
# Helper: list users (optional)
# -----------------------------
def list_users():
    """Return all registered users (for admin/debug)."""
    init_db()
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, email, full_name, created_at FROM users ORDER BY id DESC;")
    users = [dict(row) for row in cur.fetchall()]
    conn.close()
    return users
