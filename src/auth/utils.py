
from passlib.context import CryptContext

password_context = CryptContext(
    schemes=['bcrypt'],
    deprecated="auto"
)

def generate_password_hash(password: str) -> str:
    """
    Generate bcrypt hash from plain password.
    Automatically truncates to 72 bytes (bcrypt limit).
    """
    # Truncate to 72 bytes if necessary (bcrypt limit)
    if len(password.encode('utf-8')) > 72:
        password = password[:72]  # ✅ Truncate to 72 characters
    
    hash_value = password_context.hash(password)
    return hash_value

def verify_password(password: str, hash: str) -> bool:
    """
    Verify a password against its hash.
    Automatically truncates to 72 bytes if necessary.
    """
    # Truncate to 72 bytes if necessary
    if len(password.encode('utf-8')) > 72:
        password = password[:72]
    
    return password_context.verify(password, hash)