from fastapi import FastAPI, APIRouter, HTTPException, Depends, Header
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from typing import List, Optional
import uuid
from datetime import datetime
import random

from models import (
    UserCreate, UserLogin, UserResponse, TokenResponse,
    Question, QuestionResponse, QuestionOption,
    SimulationAnswer, SimulationSubmit, SimulationResult, SimulationHistoryItem,
    ModuleInfo, ModuleQuestion
)
from auth import hash_password, verify_password, create_access_token, decode_access_token
from database import db, users_collection, questions_collection, simulations_collection, init_db

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI(title="Detran Quiz API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== Auth Dependency ====================
async def get_current_user(authorization: str = Header(None)):
    """Verify JWT token and return current user"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Esquema de autenticação inválido")
    except ValueError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token expirado ou inválido")
    
    user_id = payload.get("user_id")
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    
    return user

# ==================== Health Check ====================
@api_router.get("/")
async def root():
    return {"message": "Detran Quiz API - Bem-vindo!", "status": "online"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# ==================== Auth Routes ====================
@api_router.post("/auth/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    """Register a new user"""
    # Check if user exists
    existing_user = await users_collection.find_one({"email": user_data.email.lower()})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    # Create user
    user_id = str(uuid.uuid4())
    hashed_password = hash_password(user_data.password)
    
    user_doc = {
        "_id": user_id,
        "email": user_data.email.lower(),
        "password": hashed_password,
        "name": user_data.name,
        "created_at": datetime.utcnow()
    }
    
    await users_collection.insert_one(user_doc)
    
    # Create token
    access_token = create_access_token({"user_id": user_id, "email": user_data.email.lower()})
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=user_id,
            email=user_data.email.lower(),
            name=user_data.name,
            created_at=user_doc["created_at"]
        )
    )

@api_router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Login user and return token"""
    user = await users_collection.find_one({"email": credentials.email.lower()})
    if not user:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    if not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    access_token = create_access_token({"user_id": user["_id"], "email": user["email"]})
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=user["_id"],
            email=user["email"],
            name=user["name"],
            created_at=user["created_at"]
        )
    )

@api_router.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user info"""
    return UserResponse(
        id=current_user["_id"],
        email=current_user["email"],
        name=current_user["name"],
        created_at=current_user["created_at"]
    )

# ==================== Module Routes ====================
@api_router.get("/modules", response_model=List[ModuleInfo])
async def get_modules():
    """Get all modules with their info"""
    modules = [
        ModuleInfo(
            modulo="1",
            name="Placas, Cores e Caminhos",
            difficulty="fácil",
            total_questions=await questions_collection.count_documents({"modulo": "1"})
        ),
        ModuleInfo(
            modulo="2",
            name="Escolhas e Consequências",
            difficulty="intermediário",
            total_questions=await questions_collection.count_documents({"modulo": "2"})
        ),
        ModuleInfo(
            modulo="3",
            name="Na Direção da Segurança",
            difficulty="difícil",
            total_questions=await questions_collection.count_documents({"modulo": "3"})
        ),
        ModuleInfo(
            modulo="4",
            name="Cuidar, Agir e Preservar",
            difficulty="fácil",
            total_questions=await questions_collection.count_documents({"modulo": "4"})
        )
    ]
    return modules

@api_router.get("/modules/{modulo}/questions", response_model=List[QuestionResponse])
async def get_module_questions(modulo: str, limit: int = 10, skip: int = 0):
    """Get questions from a specific module"""
    if modulo not in ["1", "2", "3", "4"]:
        raise HTTPException(status_code=400, detail="Módulo inválido")
    
    questions = await questions_collection.find({"modulo": modulo}).skip(skip).limit(limit).to_list(limit)
    
    return [
        QuestionResponse(
            id=q["_id"],
            modulo=q["modulo"],
            numero=q["numero"],
            questao=q["questao"],
            alternativas=QuestionOption(**q["alternativas"]),
            has_image=q.get("has_image", False),
            image_placeholder=q.get("image_placeholder")
        )
        for q in questions
    ]

@api_router.get("/modules/{modulo}/question/{question_id}", response_model=ModuleQuestion)
async def get_module_question_with_answer(modulo: str, question_id: str):
    """Get a specific question with answer (for study mode)"""
    question = await questions_collection.find_one({"_id": question_id, "modulo": modulo})
    if not question:
        raise HTTPException(status_code=404, detail="Questão não encontrada")
    
    return ModuleQuestion(
        question=QuestionResponse(
            id=question["_id"],
            modulo=question["modulo"],
            numero=question["numero"],
            questao=question["questao"],
            alternativas=QuestionOption(**question["alternativas"]),
            has_image=question.get("has_image", False),
            image_placeholder=question.get("image_placeholder")
        ),
        correct_answer=question["resposta"],
        comment=question["comentario"]
    )

# ==================== Simulation Routes ====================
@api_router.get("/simulation/new", response_model=List[QuestionResponse])
async def start_new_simulation(
    current_user: dict = Depends(get_current_user),
    modules: str = None,
    count: int = 30
):
    """Start a new simulation with random questions.
    modules: comma-separated module numbers (e.g., '1,2,3')
    count: number of questions (default 30)
    """
    count = min(max(count, 10), 50)  # Between 10 and 50
    
    query = {}
    if modules:
        module_list = [m.strip() for m in modules.split(',') if m.strip() in ['1','2','3','4']]
        if module_list:
            query["modulo"] = {"$in": module_list}
    
    all_questions = await questions_collection.find(query).to_list(None)
    
    if len(all_questions) < count:
        raise HTTPException(status_code=400, detail=f"Não há questões suficientes. Disponíveis: {len(all_questions)}")
    
    selected_questions = random.sample(all_questions, count)
    
    return [
        QuestionResponse(
            id=q["_id"],
            modulo=q["modulo"],
            numero=q["numero"],
            questao=q["questao"],
            alternativas=QuestionOption(**q["alternativas"]),
            has_image=q.get("has_image", False),
            image_placeholder=q.get("image_placeholder")
        )
        for q in selected_questions
    ]

@api_router.post("/simulation/submit", response_model=SimulationResult)
async def submit_simulation(
    submission: SimulationSubmit,
    current_user: dict = Depends(get_current_user)
):
    """Submit simulation answers and get results"""
    total_questions = len(submission.answers)
    if total_questions < 10 or total_questions > 50:
        raise HTTPException(status_code=400, detail="O simulado deve ter entre 10 e 50 questões")
    
    # Calculate score
    correct_count = 0
    answers_review = []
    
    for answer in submission.answers:
        question = await questions_collection.find_one({"_id": answer.question_id})
        if not question:
            continue
        
        is_correct = answer.selected_option == question["resposta"]
        if is_correct:
            correct_count += 1
        
        answers_review.append({
            "question_id": answer.question_id,
            "questao": question["questao"],
            "modulo": question.get("modulo", ""),
            "selected_option": answer.selected_option,
            "correct_answer": question["resposta"],
            "is_correct": is_correct,
            "comentario": question["comentario"],
            "alternativas": question["alternativas"]
        })
    
    score = (correct_count / total_questions) * 100
    passed = score >= 70  # 70% to pass
    
    # Save simulation result
    simulation_id = str(uuid.uuid4())
    simulation_doc = {
        "_id": simulation_id,
        "user_id": current_user["_id"],
        "score": score,
        "correct_answers": correct_count,
        "total_questions": total_questions,
        "passed": passed,
        "time_taken_seconds": submission.time_taken_seconds,
        "answers_review": answers_review,
        "created_at": datetime.utcnow()
    }
    
    await simulations_collection.insert_one(simulation_doc)
    
    return SimulationResult(
        id=simulation_id,
        user_id=current_user["_id"],
        score=score,
        correct_answers=correct_count,
        total_questions=30,
        passed=passed,
        time_taken_seconds=submission.time_taken_seconds,
        created_at=simulation_doc["created_at"],
        answers_review=answers_review
    )

@api_router.get("/simulation/{simulation_id}", response_model=SimulationResult)
async def get_simulation_result(
    simulation_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific simulation result"""
    simulation = await simulations_collection.find_one({
        "_id": simulation_id,
        "user_id": current_user["_id"]
    })
    
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulado não encontrado")
    
    return SimulationResult(
        id=simulation["_id"],
        user_id=simulation["user_id"],
        score=simulation["score"],
        correct_answers=simulation["correct_answers"],
        total_questions=simulation["total_questions"],
        passed=simulation["passed"],
        time_taken_seconds=simulation["time_taken_seconds"],
        created_at=simulation["created_at"],
        answers_review=simulation.get("answers_review")
    )

# ==================== History Routes ====================
@api_router.get("/history", response_model=List[SimulationHistoryItem])
async def get_user_history(
    current_user: dict = Depends(get_current_user),
    limit: int = 20
):
    """Get user's simulation history"""
    simulations = await simulations_collection.find(
        {"user_id": current_user["_id"]}
    ).sort("created_at", -1).limit(limit).to_list(limit)
    
    return [
        SimulationHistoryItem(
            id=sim["_id"],
            score=sim["score"],
            passed=sim["passed"],
            time_taken_seconds=sim["time_taken_seconds"],
            created_at=sim["created_at"]
        )
        for sim in simulations
    ]

@api_router.get("/stats")
async def get_user_stats(current_user: dict = Depends(get_current_user)):
    """Get user's statistics"""
    simulations = await simulations_collection.find(
        {"user_id": current_user["_id"]}
    ).to_list(None)
    
    if not simulations:
        return {
            "total_simulations": 0,
            "passed_simulations": 0,
            "average_score": 0,
            "best_score": 0,
            "total_questions_answered": 0,
            "pass_rate": 0
        }
    
    total = len(simulations)
    passed = sum(1 for s in simulations if s["passed"])
    scores = [s["score"] for s in simulations]
    
    return {
        "total_simulations": total,
        "passed_simulations": passed,
        "average_score": round(sum(scores) / total, 2),
        "best_score": max(scores),
        "total_questions_answered": sum(s.get("total_questions", 30) for s in simulations),
        "pass_rate": round((passed / total) * 100, 2) if total > 0 else 0
    }

# ==================== Missed Questions Routes ====================
@api_router.get("/missed-questions")
async def get_missed_questions(current_user: dict = Depends(get_current_user)):
    """Get all questions the user has answered incorrectly in simulations"""
    simulations = await simulations_collection.find(
        {"user_id": current_user["_id"]}
    ).sort("created_at", -1).to_list(None)
    
    if not simulations:
        return {"questions": [], "total_missed": 0}
    
    # Collect all missed question IDs (unique)
    missed_ids = set()
    correct_ids = set()
    
    for sim in simulations:
        for answer in sim.get("answers_review", []):
            qid = answer.get("question_id")
            if answer.get("is_correct"):
                correct_ids.add(qid)
            else:
                missed_ids.add(qid)
    
    # Only include questions that were missed and never answered correctly after
    still_missed = missed_ids - correct_ids
    
    if not still_missed:
        return {"questions": [], "total_missed": 0}
    
    # Fetch the full question data
    questions_cursor = questions_collection.find({"_id": {"$in": list(still_missed)}})
    questions = await questions_cursor.to_list(None)
    
    result = []
    for q in questions:
        result.append({
            "id": q["_id"],
            "modulo": q["modulo"],
            "numero": q.get("numero", ""),
            "questao": q["questao"],
            "alternativas": q["alternativas"],
        })
    
    return {"questions": result, "total_missed": len(result)}

@api_router.get("/stats/by-module")
async def get_stats_by_module(current_user: dict = Depends(get_current_user)):
    """Get user statistics grouped by module"""
    simulations = await simulations_collection.find(
        {"user_id": current_user["_id"]}
    ).to_list(None)
    
    module_stats = {}
    for mod in ["1", "2", "3", "4"]:
        module_stats[mod] = {"total": 0, "correct": 0, "incorrect": 0}
    
    for sim in simulations:
        for answer in sim.get("answers_review", []):
            modulo = answer.get("modulo", "")
            if not modulo:
                # Try to find module from question
                q = await questions_collection.find_one({"_id": answer.get("question_id")})
                if q:
                    modulo = q.get("modulo", "")
            if modulo in module_stats:
                module_stats[modulo]["total"] += 1
                if answer.get("is_correct"):
                    module_stats[modulo]["correct"] += 1
                else:
                    module_stats[modulo]["incorrect"] += 1
    
    result = {}
    for mod, stats in module_stats.items():
        result[mod] = {
            **stats,
            "accuracy": round((stats["correct"] / stats["total"]) * 100, 1) if stats["total"] > 0 else 0
        }
    
    return result

# ==================== Admin Routes (for seeding) ====================
@api_router.get("/questions/count")
async def get_questions_count():
    """Get total number of questions in database"""
    total = await questions_collection.count_documents({})
    by_module = {
        "1": await questions_collection.count_documents({"modulo": "1"}),
        "2": await questions_collection.count_documents({"modulo": "2"}),
        "3": await questions_collection.count_documents({"modulo": "3"}),
        "4": await questions_collection.count_documents({"modulo": "4"})
    }
    return {"total": total, "by_module": by_module}

# ==================== Bookmarks Routes ====================
@api_router.get("/bookmarks")
async def get_bookmarks(current_user: dict = Depends(get_current_user)):
    """Get user's bookmarked question IDs"""
    user = await users_collection.find_one({"_id": current_user["_id"]})
    return {"bookmarks": user.get("bookmarks", [])}

@api_router.post("/bookmarks/{question_id}")
async def toggle_bookmark(question_id: str, current_user: dict = Depends(get_current_user)):
    """Toggle bookmark on a question"""
    user = await users_collection.find_one({"_id": current_user["_id"]})
    bookmarks = user.get("bookmarks", [])
    
    if question_id in bookmarks:
        bookmarks.remove(question_id)
        action = "removed"
    else:
        bookmarks.append(question_id)
        action = "added"
    
    await users_collection.update_one(
        {"_id": current_user["_id"]},
        {"$set": {"bookmarks": bookmarks}}
    )
    
    return {"action": action, "bookmarks": bookmarks}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_db()
    logger.info("Database initialized")

@app.on_event("shutdown")
async def shutdown_db_client():
    from database import client
    client.close()
