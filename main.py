from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
import uuid
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional

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

# --- Pydantic Schemas ---

class ModuleBase(BaseModel):
    name: str
    description: Optional[str] = None

class ModuleCreate(ModuleBase):
    pass

class ModuleUpdate(ModuleBase):
    pass

class ModuleRead(ModuleBase):
    id: str
    class Config:
        orm_mode = True

# --- CRUD Endpoints for Module ---

@app.post("/modules/", response_model=ModuleRead)
def create_module(module: ModuleCreate, db: Session = Depends(get_db)):
    db_module = Module(name=module.name, description=module.description)
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module

@app.get("/modules/", response_model=List[ModuleRead])
def read_modules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    modules = db.query(Module).offset(skip).limit(limit).all()
    return modules

@app.get("/modules/{module_id}", response_model=ModuleRead)
def read_module(module_id: str, db: Session = Depends(get_db)):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        return {"error": "Module not found"}
    return module

@app.put("/modules/{module_id}", response_model=ModuleRead)
def update_module(module_id: str, module: ModuleUpdate, db: Session = Depends(get_db)):
    db_module = db.query(Module).filter(Module.id == module_id).first()
    if not db_module:
        return {"error": "Module not found"}
    db_module.name = module.name
    db_module.description = module.description
    db.commit()
    db.refresh(db_module)
    return db_module

@app.delete("/modules/{module_id}")
def delete_module(module_id: str, db: Session = Depends(get_db)):
    db_module = db.query(Module).filter(Module.id == module_id).first()
    if not db_module:
        return {"error": "Module not found"}
    db.delete(db_module)
    db.commit()
    return {"ok": True}
