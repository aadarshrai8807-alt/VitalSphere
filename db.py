# db.py
from sqlmodel import create_engine, SQLModel, Session

# For demo use sqlite file; replace with PostgreSQL in production:
DATABASE_URL = "sqlite:///./vitalsphere_demo.db"
# Example Postgres: "postgresql://user:pass@db:5432/vitasphere"

engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def init_db():
    from models import SQLModel  # ensure models are imported elsewhere
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)