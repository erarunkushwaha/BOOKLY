import bcrypt


def generate_password_hash(password: str) -> str:
    """
    Generate bcrypt hash from plain password.
    Automatically truncates to 72 bytes (bcrypt limit).
    """
    # Encode password to bytes
    password_bytes = password.encode('utf-8')
    
    # Truncate to 72 bytes if necessary (bcrypt limit)
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(password_bytes, salt)
    
    # Return as string
    return hash_bytes.decode('utf-8')


def verify_password(password: str, hash: str) -> bool:
    """
    Verify a password against its hash.
    Automatically truncates to 72 bytes if necessary.
    """
    # Encode password and hash to bytes
    password_bytes = password.encode('utf-8')
    hash_bytes = hash.encode('utf-8')
    
    # Truncate password to 72 bytes if necessary
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Verify password
    return bcrypt.checkpw(password_bytes, hash_bytes)