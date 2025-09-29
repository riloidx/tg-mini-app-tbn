from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_telegram_init_data
from app.db.base import get_db
from app.db.crud import create_or_update_user


async def get_current_user(
    x_init_data: str = Header(..., alias="X-Init-Data"),
    db: AsyncSession = Depends(get_db)
) -> dict:
    validation_result = verify_telegram_init_data(x_init_data)
    
    if not validation_result.is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid init data: {validation_result.error}",
        )
    
    user_data = validation_result.user
    user = await create_or_update_user(
        db=db,
        telegram_id=user_data.id,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username
    )
    
    return {
        "user_id": user.id,
        "telegram_id": user.telegram_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username
    }