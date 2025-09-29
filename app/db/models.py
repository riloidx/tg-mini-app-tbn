from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Integer, String, Text, TIMESTAMP, CheckConstraint, ForeignKey, DECIMAL, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(Text)
    last_name: Mapped[Optional[str]] = mapped_column(Text)
    username: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    last_seen_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True))
    last_test_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True))
    
    results: Mapped[list["Result"]] = relationship("Result", back_populates="user")


class Result(Base):
    __tablename__ = "results"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="RESTRICT"))
    taken_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    total_score: Mapped[int] = mapped_column(Integer, nullable=False)
    happiness_score: Mapped[int] = mapped_column(Integer, nullable=False)
    selfreal_score: Mapped[int] = mapped_column(Integer, nullable=False)
    freedom_score: Mapped[int] = mapped_column(Integer, nullable=False)
    happiness_pct: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    selfreal_pct: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    freedom_pct: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    version: Mapped[str] = mapped_column(Text, nullable=False)
    meta: Mapped[Optional[dict]] = mapped_column(JSON)
    
    user: Mapped["User"] = relationship("User", back_populates="results")


class Question(Base):
    __tablename__ = "questions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(Text, nullable=False)
    max_points: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    
    options: Mapped[list["QuestionOption"]] = relationship("QuestionOption", back_populates="question")
    
    __table_args__ = (
        CheckConstraint("category IN ('happiness','selfreal','freedom')", name="check_category"),
    )


class QuestionOption(Base):
    __tablename__ = "question_options"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))
    label: Mapped[str] = mapped_column(Text, nullable=False)
    points: Mapped[int] = mapped_column(Integer, nullable=False)
    sort_index: Mapped[int] = mapped_column(Integer, nullable=False)
    
    question: Mapped["Question"] = relationship("Question", back_populates="options")