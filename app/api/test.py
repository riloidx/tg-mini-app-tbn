from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.crud import get_questions_with_options, can_take_test, create_result, get_user_by_id
from app.schemas.test import (
    Question, QuestionOption, TestMeta, TestSubmission, 
    TestSubmissionResponse
)
from app.api.dependencies import get_current_user

router = APIRouter()


@router.get("/meta", response_model=TestMeta)
async def get_test_meta(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return TestMeta(
        version="v1",
        total_questions=51,
        categories={
            "happiness": {"start": 1, "end": 36, "count": 36},
            "selfreal": {"start": 37, "end": 46, "count": 10},
            "freedom": {"start": 47, "end": 51, "count": 5}
        },
        max_scores={
            "happiness": 42,
            "selfreal": 48,
            "freedom": 10,
            "total": 100
        },
        rules={
            "frequency": "1 раз в 10 дней",
            "scoring": "1 балл = 1%"
        }
    )


@router.get("/questions", response_model=List[Question])
async def get_questions(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    questions = await get_questions_with_options(db)
    
    return [
        Question(
            id=q.id,
            number=q.number,
            text=q.text,
            options=[
                QuestionOption(
                    id=opt.id,
                    label=opt.label,
                    points=opt.points
                )
                for opt in sorted(q.options, key=lambda x: x.sort_index)
            ]
        )
        for q in questions
    ]


@router.post("/submit", response_model=TestSubmissionResponse)
async def submit_test(
    submission: TestSubmission,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_id = current_user["user_id"]
    
    # Check if user exists
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found. Please authenticate first."
        )
    
    # Check if user can take test
    if not await can_take_test(db, user_id):
        next_allowed = datetime.utcnow() + timedelta(days=10)
        return TestSubmissionResponse(
            ok=False,
            error="Test can only be taken once every 10 days",
            next_allowed_at=next_allowed.isoformat()
        )
    
    # Validate scores
    happiness_score = submission.scores_by_category.get("happiness", 0)
    selfreal_score = submission.scores_by_category.get("selfreal", 0)
    freedom_score = submission.scores_by_category.get("freedom", 0)
    
    calculated_total = happiness_score + selfreal_score + freedom_score
    
    if calculated_total != submission.total_score:
        raise HTTPException(
            status_code=400,
            detail="Total score doesn't match sum of category scores"
        )
    
    # Validate score ranges
    if not (0 <= happiness_score <= 42):
        raise HTTPException(status_code=400, detail="Invalid happiness score")
    if not (0 <= selfreal_score <= 48):
        raise HTTPException(status_code=400, detail="Invalid selfreal score")
    if not (0 <= freedom_score <= 10):
        raise HTTPException(status_code=400, detail="Invalid freedom score")
    
    # Create result
    await create_result(
        db=db,
        user_id=user_id,
        total_score=submission.total_score,
        happiness_score=happiness_score,
        selfreal_score=selfreal_score,
        freedom_score=freedom_score,
        version=submission.version
    )
    
    next_allowed = datetime.utcnow() + timedelta(days=10)
    
    return TestSubmissionResponse(
        ok=True,
        next_allowed_at=next_allowed.isoformat()
    )