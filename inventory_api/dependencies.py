import os
from fastapi.security import HTTPBearer
import bcrypt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from inventory_api.database import SessionLocal
import random
import string


security = HTTPBearer()
secret_key = os.getenv("SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception


def require_role(role: str):
    def role_dependency(current_user: dict = Depends(get_current_user)):
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )
        if current_user["role"] != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted",
            )
        return current_user
    return role_dependency


def hash_password(password: str):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def generate_random_name(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))
