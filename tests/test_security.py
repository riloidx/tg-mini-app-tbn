import hashlib
import hmac
import json
import time
from urllib.parse import urlencode

import pytest
from app.core.security import verify_telegram_init_data
from app.core.config import settings


def create_valid_init_data(user_data: dict, bot_token: str) -> str:
    auth_date = int(time.time())
    
    data = {
        'user': json.dumps(user_data),
        'auth_date': str(auth_date)
    }
    
    # Create data_check_string
    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(data.items())])
    
    # Calculate secret key and hash
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    
    data['hash'] = calculated_hash
    
    return urlencode(data)


def test_valid_init_data():
    user_data = {
        'id': 123456789,
        'first_name': 'Test',
        'last_name': 'User',
        'username': 'testuser'
    }
    
    init_data = create_valid_init_data(user_data, settings.telegram_bot_token)
    result = verify_telegram_init_data(init_data)
    
    assert result.is_valid is True
    assert result.user is not None
    assert result.user.id == 123456789
    assert result.user.first_name == 'Test'


def test_invalid_hash():
    user_data = {
        'id': 123456789,
        'first_name': 'Test'
    }
    
    init_data = create_valid_init_data(user_data, settings.telegram_bot_token)
    # Corrupt the hash
    init_data = init_data.replace(init_data.split('hash=')[1][:10], 'invalid123')
    
    result = verify_telegram_init_data(init_data)
    
    assert result.is_valid is False
    assert result.error == "Invalid hash"


def test_old_auth_date():
    user_data = {
        'id': 123456789,
        'first_name': 'Test'
    }
    
    # Create init_data with old timestamp
    old_auth_date = int(time.time()) - 90000  # More than 24 hours ago
    
    data = {
        'user': json.dumps(user_data),
        'auth_date': str(old_auth_date)
    }
    
    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(data.items())])
    secret_key = hashlib.sha256(settings.telegram_bot_token.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    
    data['hash'] = calculated_hash
    init_data = urlencode(data)
    
    result = verify_telegram_init_data(init_data)
    
    assert result.is_valid is False
    assert result.error == "Data is too old"


def test_missing_hash():
    init_data = "user=%7B%22id%22%3A123456789%7D&auth_date=1234567890"
    result = verify_telegram_init_data(init_data)
    
    assert result.is_valid is False
    assert result.error == "Hash not found"