# auth.py
# 整个登录逻辑似乎只允许用户在一个网页登录，否则，第二个网页的登录会覆盖第一个网页的登录，这个问题以后再解决
# 除此之外，很多地方都是直接使用假数据库，以后要改成ORM

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from models.users import UserInDB, Token

SECRET_KEY = "a_very_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
)

# 用于测试的假用户数据库

fake_users_db = {
    "admin1": {
        "username": "admin1",
        "hashed_password": pwd_context.hash("admin"),
        "role": "admin",
        "valid_from": datetime(2021, 1, 1),
        "valid_until": datetime(2025, 1, 1),
        "token": None
    },
    "student1": {
        "username": "student1",
        "hashed_password": pwd_context.hash("student"),
        "role": "student",
        "valid_from": datetime(2021, 1, 1),
        "valid_until": datetime(2025, 1, 1),
        "token": None
    }
}

def invalidate_token(token: str):
    user = [user for user in fake_users_db.values() if user["token"] == token]
    if user:
        user[0]["token"] = None
    else:
        raise Exception("Token not found")

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

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
        token_data = username
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, token_data)
    if user is None or user.token != token:
        raise credentials_exception
    return user