"""Authentication: user registration, password hashing, and session tokens.

This module has no dependencies on other ShopLite modules. Every other module that
needs to know who is calling goes through verify_token().
"""
import hashlib
import hmac
import secrets
import time

TOKEN_TTL_SECONDS = 60 * 60

_users = {}   # username -> (salt, password_hash)
_tokens = {}  # token -> (username, expires_at)


def _hash_password(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)


def register_user(username, password):
    """Create a user. Raises ValueError if the username is already taken."""
    if username in _users:
        raise ValueError("username already exists")
    salt = secrets.token_bytes(16)
    _users[username] = (salt, _hash_password(password, salt))


def user_exists(username):
    """Return True if the username is registered."""
    return username in _users


def login(username, password):
    """Return a session token, or None if the credentials are wrong."""
    record = _users.get(username)
    if record is None:
        return None
    salt, stored = record
    if not hmac.compare_digest(stored, _hash_password(password, salt)):
        return None
    token = secrets.token_hex(16)
    _tokens[token] = (username, time.time() + TOKEN_TTL_SECONDS)
    return token


def verify_token(token):
    """Return the username for a valid, unexpired token, else None."""
    entry = _tokens.get(token)
    if entry is None:
        return None
    username, expires_at = entry
    if time.time() > expires_at:
        del _tokens[token]
        return None
    return username
