from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel


class QuestionOption(BaseModel):
    id: int
    label: str
    points: int


class Question(BaseModel):
    id: int
    number: int
    text: str
    options: List[QuestionOption]


class TestMeta(BaseModel):
    version: str
    total_questions: int
    categories: Dict[str, Dict[str, int]]
    max_scores: Dict[str, int]
    rules: Dict[str, str]


class TestSubmission(BaseModel):
    version: str = "v1"
    total_score: int
    scores_by_category: Dict[str, int]


class TestSubmissionResponse(BaseModel):
    ok: bool
    next_allowed_at: Optional[str] = None
    error: Optional[str] = None


class ResultResponse(BaseModel):
    id: int
    taken_at: datetime
    total_score: int
    happiness_score: int
    selfreal_score: int
    freedom_score: int
    happiness_pct: float
    selfreal_pct: float
    freedom_pct: float
    version: str