import os
from databases import Database
from sqlalchemy import MetaData, create_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/right_to_choice")

database = Database(DATABASE_URL)
metadata = MetaData()

sync_engine = create_engine(DATABASE_URL.replace("+asyncpg", ""), echo=False)

