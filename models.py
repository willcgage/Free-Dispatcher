
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
import uuid

DATABASE_URL = "sqlite:///./test.db"  # Change to PostgreSQL URL for cloud

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

# Models
class Module(Base):
    __tablename__ = "modules"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
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
    name = Column(String)
    position = Column(String)
    module = relationship("Module", back_populates="signals")

class Switch(Base):
    __tablename__ = "switches"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    module_id = Column(String, ForeignKey("modules.id"))
    name = Column(String)
    type = Column(String)
    module = relationship("Module", back_populates="switches")

class Block(Base):
    __tablename__ = "blocks"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    start_module_id = Column(String, ForeignKey("modules.id"))
    end_module_id = Column(String, ForeignKey("modules.id"))

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Free-Dispatcher App"}
