from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

# ==================== User Models ====================
class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# ==================== Question Models ====================
class QuestionOption(BaseModel):
    A: str
    B: str
    C: str
    D: str

class Question(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    modulo: str
    numero: str
    questao: str
    alternativas: QuestionOption
    resposta: str
    comentario: str
    has_image: bool = False
    image_placeholder: Optional[str] = None

class QuestionResponse(BaseModel):
    id: str
    modulo: str
    numero: str
    questao: str
    alternativas: QuestionOption
    has_image: bool
    image_placeholder: Optional[str]

# ==================== Simulation Models ====================
class SimulationAnswer(BaseModel):
    question_id: str
    selected_option: str  # A, B, C, D

class SimulationSubmit(BaseModel):
    answers: List[SimulationAnswer]
    time_taken_seconds: int

class SimulationResult(BaseModel):
    id: str
    user_id: str
    score: float
    correct_answers: int
    total_questions: int
    passed: bool
    time_taken_seconds: int
    created_at: datetime
    answers_review: Optional[List[dict]] = None

class SimulationHistoryItem(BaseModel):
    id: str
    score: float
    passed: bool
    time_taken_seconds: int
    created_at: datetime

# ==================== Module Study Models ====================
class ModuleInfo(BaseModel):
    modulo: str
    name: str
    difficulty: str
    total_questions: int

class ModuleQuestion(BaseModel):
    question: QuestionResponse
    correct_answer: str
    comment: str
