import hashlib
import hmac
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from urllib.parse import parse_qsl, unquote

from jose import JWTError, jwt
from pydantic import BaseModel

from .config import settings


class TelegramUser(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None


class InitDataValidationResult(BaseModel):
    is_valid: bool
    user: Optional[TelegramUser] = None
    error: Optional[str] = None


def verify_telegram_init_data(init_data: str) -> InitDataValidationResult:
    try:
        # Parse init_data
        parsed_data = dict(parse_qsl(init_data))
        
        if "hash" not in parsed_data:
            return InitDataValidationResult(is_valid=False, error="Hash not found")
        
        received_hash = parsed_data.pop("hash")
        
        # Check auth_date
        if "auth_date" not in parsed_data:
            return InitDataValidationResult(is_valid=False, error="Auth date not found")
        
        auth_date = int(parsed_data["auth_date"])
        current_time = int(time.time())
        
        if current_time - auth_date > settings.initdata_max_age_seconds:
            return InitDataValidationResult(is_valid=False, error="Data is too old")
        
        # Create data_check_string
        data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(parsed_data.items())])
        
        # Calculate secret key
        secret_key = hashlib.sha256(settings.telegram_bot_token.encode()).digest()
        
        # Calculate HMAC
        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if calculated_hash != received_hash:
            return InitDataValidationResult(is_valid=False, error="Invalid hash")
        
        # Parse user data
        if "user" not in parsed_data:
            return InitDataValidationResult(is_valid=False, error="User data not found")
        
        user_data = json.loads(unquote(parsed_data["user"]))
        user = TelegramUser(**user_data)
        
        return InitDataValidationResult(is_valid=True, user=user)
        
    except Exception as e:
        return InitDataValidationResult(is_valid=False, error=f"Validation error: {str(e)}")


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return payload
    except JWTError:
        return None