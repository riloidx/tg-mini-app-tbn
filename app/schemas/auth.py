from typing import Optional
from pydantic import BaseModel


class InitDataRequest(BaseModel):
    init_data: str


class UserResponse(BaseModel):
    telegram_id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None


class AuthResponse(BaseModel):
    ok: bool
    user: Optional[UserResponse] = None
    error: Optional[str] = None