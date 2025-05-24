from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
import uuid
import os
from dotenv import load_dotenv

# Load environment variables from .env file, if present
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please check your environment variables or .env file.")

# Set up SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

# --- SQLAlchemy Models ---

class Module(Base):
    __tablename__ = "modules"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    endplates = relationship("Endplate", back_populates="module")
    signals = relationship("Signal", back_populates="module")
    switches = relationship("Switch", back_populates="module")

class Endplate(Base):
    __tablename__ = "endplates"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    module_id = Column(String, ForeignKey("modules.id"))
    position = Column(Integer)
    is_block_end = Column(Boolean, default=False)
    module = relationship("Module", back_populates="endplates")

class Signal(Base):
    __tablename__ = "signals"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    module_id = Column(String, ForeignKey("modules.id"))
    name = Column(String, nullable=False)
    position = Column(String)
    module = relationship("Module", back_populates="signals")

class Switch(Base):
    __tablename__ = "switches"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    module_id = Column(String, ForeignKey("modules.id"))
    name = Column(String, nullable=False)
    type = Column(String)
    module = relationship("Module", back_populates="switches")

class Block(Base):
    __tablename__ = "blocks"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    start_module_id = Column(String, ForeignKey("modules.id"))
    end_module_id = Column(String, ForeignKey("modules.id"))

    start_module = relationship("Module", foreign_keys=[start_module_id], backref="start_blocks")
    end_module = relationship("Module", foreign_keys=[end_module_id], backref="end_blocks")

# Create all tables in the database (for development only; use Alembic in production)
# Base.metadata.create_all(bind=engine)

# --- FastAPI Dependency for DB Session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Free-Dispatcher App"}
