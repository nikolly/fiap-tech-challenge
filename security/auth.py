from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
from dotenv import load_dotenv
import bcrypt
import os

from core.functions.functions import load_users_from_json

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

class Auth:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encoded_jwt


    def verify_password(self, password: str, hashed_password: str) -> bool:
        
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


    def get_current_user(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        user = load_users_from_json("data/users.json")
        if not user:
            raise credentials_exception
        
        return user[username]


    def authenticate_user(self, username: str, password: str):
        user = load_users_from_json("data/users.json")
        
        if not user or username not in user:
            return False
        
        return False if not self.verify_password(password, user[username]["hashed_password"]) else user[username]
