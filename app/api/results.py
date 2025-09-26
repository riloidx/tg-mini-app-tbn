from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.crud import get_user_results
from app.schemas.test import ResultResponse
from app.api.dependencies import get_current_user

router = APIRouter()


@router.get("/me", response_model=List[ResultResponse])
async def get_my_results(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_id = current_user["user_id"]
    results = await get_user_results(db, user_id)
    
    return [
        ResultResponse(
            id=result.id,
            taken_at=result.taken_at,
            total_score=result.total_score,
            happiness_score=result.happiness_score,
            selfreal_score=result.selfreal_score,
            freedom_score=result.freedom_score,
            happiness_pct=float(result.happiness_pct),
            selfreal_pct=float(result.selfreal_pct),
            freedom_pct=float(result.freedom_pct),
            version=result.version
        )
        for result in results
    ]