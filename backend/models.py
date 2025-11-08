from pydantic import BaseModel, Field  # type: ignore
from typing import List, Optional

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: str
    explanation: Optional[str] = None

class QuizOutput(BaseModel):
    article_title: str
    summary: str
    questions: List[QuizQuestion]
    key_entities: Optional[List[str]] = None
    related_topics: Optional[List[str]] = None