from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    role: str
    valid_from: datetime
    valid_until: datetime
    token: Optional[str] = None


