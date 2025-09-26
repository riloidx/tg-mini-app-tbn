from datetime import datetime, timedelta
from unittest.mock import AsyncMock

import pytest
from app.db.crud import can_take_test
from app.db.models import User


@pytest.mark.asyncio
async def test_can_take_test_new_user():
    # Mock database session
    db_mock = AsyncMock()
    
    # Mock user with no previous test
    user = User(id=1, telegram_id=123, last_test_at=None)
    db_mock.get.return_value = user
    
    result = await can_take_test(db_mock, 1)
    assert result is True


@pytest.mark.asyncio
async def test_can_take_test_within_10_days():
    # Mock database session
    db_mock = AsyncMock()
    
    # Mock user with recent test (5 days ago)
    recent_test = datetime.utcnow() - timedelta(days=5)
    user = User(id=1, telegram_id=123, last_test_at=recent_test)
    db_mock.get.return_value = user
    
    result = await can_take_test(db_mock, 1)
    assert result is False


@pytest.mark.asyncio
async def test_can_take_test_after_10_days():
    # Mock database session
    db_mock = AsyncMock()
    
    # Mock user with old test (15 days ago)
    old_test = datetime.utcnow() - timedelta(days=15)
    user = User(id=1, telegram_id=123, last_test_at=old_test)
    db_mock.get.return_value = user
    
    result = await can_take_test(db_mock, 1)
    assert result is True


@pytest.mark.asyncio
async def test_can_take_test_exactly_10_days():
    # Mock database session
    db_mock = AsyncMock()
    
    # Mock user with test exactly 10 days ago
    exact_test = datetime.utcnow() - timedelta(days=10, seconds=1)
    user = User(id=1, telegram_id=123, last_test_at=exact_test)
    db_mock.get.return_value = user
    
    result = await can_take_test(db_mock, 1)
    assert result is True


@pytest.mark.asyncio
async def test_can_take_test_user_not_found():
    # Mock database session
    db_mock = AsyncMock()
    db_mock.get.return_value = None
    
    result = await can_take_test(db_mock, 999)
    assert result is True