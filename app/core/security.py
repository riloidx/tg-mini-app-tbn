import hashlib
import hmac
import json
import time
from typing import Optional
from urllib.parse import parse_qsl, unquote

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
        
        # Calculate secret key for WebApp init_data verification
        # Per Telegram WebApp spec: secret_key = HMAC_SHA256("WebAppData", bot_token)
        secret_key = hmac.new(
            key=b"WebAppData",
            msg=settings.telegram_bot_token.encode(),
            digestmod=hashlib.sha256
        ).digest()

        # Calculate HMAC over data_check_string with the derived secret_key
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
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