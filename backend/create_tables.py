import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import sync_engine, metadata
from backend import models

def create_all():
    try:
        with sync_engine.connect() as conn:
            pass
        
        metadata.create_all(bind=sync_engine)
        print("Tables created.")
        
        with sync_engine.connect() as conn:
            from sqlalchemy import inspect
            inspector = inspect(sync_engine)
            tables = inspector.get_table_names()
            print(f"Created tables: {', '.join(tables)}")
    except Exception as e:
        print(f"Error creating tables: {e}")
        print(f"Database URL: {os.getenv('DATABASE_URL', 'not set')}")
        raise

if __name__ == "__main__":
    create_all()

