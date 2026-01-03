import bcrypt
from datetime import timedelta,datetime
import jwt
from src.config import Config
import uuid
import logging



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

def generate_access_token(user_data:dict, expiry:timedelta | None = None , refresh: bool = False):
    payload = {}
    payload['user'] = user_data
    expiry_time = datetime.now() + (expiry if expiry is not None else timedelta(seconds=Config.ACCESS_TOKEN_EXPIRY))
    payload['exp'] = int(expiry_time.timestamp())  # Convert datetime to Unix timestamp
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    
    encoded_jwt = jwt.encode(payload=payload, key=Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    return encoded_jwt
    
    
def decode_token(token:str) -> dict | None:
    
    try:
        token_data = jwt.decode(token, key=Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        return token_data 
    
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
        
        