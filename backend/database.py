from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_url = os.environ.get('MONGO_URL')
db_name = os.environ.get('DB_NAME', 'detran_quiz')

client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

# Collections
users_collection = db.users
questions_collection = db.questions
simulations_collection = db.simulations

async def init_db():
    """Initialize database indexes"""
    # Create unique index on email
    await users_collection.create_index("email", unique=True)
    # Create index on questions by module
    await questions_collection.create_index("modulo")
    # Create index on simulations by user_id
    await simulations_collection.create_index("user_id")
