from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_telegram_init_data, create_access_token
from app.db.base import get_db
from app.db.crud import create_or_update_user
from app.schemas.auth import InitDataRequest, AuthResponse, UserResponse

router = APIRouter()


@router.post("/verify", response_model=AuthResponse)
async def verify_init_data(
    request: InitDataRequest,
    db: AsyncSession = Depends(get_db)
):
    validation_result = verify_telegram_init_data(request.init_data)
    
    if not validation_result.is_valid:
        return AuthResponse(ok=False, error=validation_result.error)
    
    user_data = validation_result.user
    user = await create_or_update_user(
        db=db,
        telegram_id=user_data.id,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username
    )
    
    token = create_access_token({"user_id": user.id, "telegram_id": user.telegram_id})
    
    return AuthResponse(
        ok=True,
        user=UserResponse(
            telegram_id=user.telegram_id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username
        ),
        token=token
    )