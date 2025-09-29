from datetime import datetime, timedelta
from typing import Optional, List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import User, Result, Question, QuestionOption


async def get_user_by_telegram_id(db: AsyncSession, telegram_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    return await db.get(User, user_id)


async def create_or_update_user(
    db: AsyncSession,
    telegram_id: int,
    first_name: str,
    last_name: Optional[str] = None,
    username: Optional[str] = None
) -> User:
    user = await get_user_by_telegram_id(db, telegram_id)
    
    if user:
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.last_seen_at = datetime.utcnow()
    else:
        user = User(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            last_seen_at=datetime.utcnow()
        )
        db.add(user)
    
    await db.commit()
    await db.refresh(user)
    return user


async def get_questions_with_options(db: AsyncSession) -> List[Question]:
    result = await db.execute(
        select(Question)
        .options(selectinload(Question.options))
        .order_by(Question.number)
    )
    return result.scalars().all()


async def can_take_test(db: AsyncSession, user_id: int) -> bool:
    user = await db.get(User, user_id)
    if not user or not user.last_test_at:
        return True
    
    ten_days_ago = datetime.utcnow() - timedelta(days=10)
    return user.last_test_at < ten_days_ago


async def create_result(
    db: AsyncSession,
    user_id: int,
    total_score: int,
    happiness_score: int,
    selfreal_score: int,
    freedom_score: int,
    version: str = "v1",
    meta: Optional[dict] = None
) -> Result:
    # Calculate percentages
    happiness_pct = round(happiness_score * 100 / 42, 2)
    selfreal_pct = round(selfreal_score * 100 / 48, 2)
    freedom_pct = round(freedom_score * 100 / 10, 2)
    
    result = Result(
        user_id=user_id,
        total_score=total_score,
        happiness_score=happiness_score,
        selfreal_score=selfreal_score,
        freedom_score=freedom_score,
        happiness_pct=happiness_pct,
        selfreal_pct=selfreal_pct,
        freedom_pct=freedom_pct,
        version=version,
        meta=meta
    )
    
    db.add(result)
    
    # Update user's last_test_at
    await db.execute(
        update(User)
        .where(User.id == user_id)
        .values(last_test_at=datetime.utcnow())
    )
    
    await db.commit()
    await db.refresh(result)
    return result


async def get_user_results(db: AsyncSession, user_id: int) -> List[Result]:
    result = await db.execute(
        select(Result)
        .where(Result.user_id == user_id)
        .order_by(Result.taken_at.desc())
    )
    return result.scalars().all()