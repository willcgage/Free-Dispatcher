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

class Dispatcher(Base):
    __tablename__ = "dispatchers"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)

class Train(Base):
    __tablename__ = "trains"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    dispatcher_id = Column(String, ForeignKey("dispatchers.id"), nullable=True)
    block_id = Column(String, ForeignKey("blocks.id"), nullable=True)  # <-- Add this line
    dispatcher = relationship("Dispatcher", backref="trains")
    block = relationship("Block", backref="trains")  # <-- Add this line

class YardMaster(Base):
    __tablename__ = "yardmasters"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)

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

class EndplateBase(BaseModel):
    module_id: str
    position: int
    is_block_end: Optional[bool] = False

class EndplateCreate(EndplateBase):
    pass

class EndplateUpdate(EndplateBase):
    pass

class EndplateRead(EndplateBase):
    id: str
    class Config:
        orm_mode = True

class SignalBase(BaseModel):
    module_id: str
    name: str
    position: Optional[str] = None

class SignalCreate(SignalBase):
    pass

class SignalUpdate(SignalBase):
    pass

class SignalRead(SignalBase):
    id: str
    class Config:
        orm_mode = True

class SwitchBase(BaseModel):
    module_id: str
    name: str
    type: Optional[str] = None

class SwitchCreate(SwitchBase):
    pass

class SwitchUpdate(SwitchBase):
    pass

class SwitchRead(SwitchBase):
    id: str
    class Config:
        orm_mode = True

class BlockBase(BaseModel):
    name: str
    start_module_id: str
    end_module_id: str

class BlockCreate(BlockBase):
    pass

class BlockUpdate(BlockBase):
    pass

class BlockRead(BlockBase):
    id: str
    class Config:
        orm_mode = True

class DispatcherBase(BaseModel):
    name: str
    email: Optional[str] = None

class DispatcherCreate(DispatcherBase):
    pass

class DispatcherUpdate(DispatcherBase):
    pass

class DispatcherRead(DispatcherBase):
    id: str
    class Config:
        orm_mode = True

class TrainBase(BaseModel):
    name: str
    description: Optional[str] = None
    dispatcher_id: Optional[str] = None
    block_id: Optional[str] = None  # <-- Add this line

class TrainCreate(TrainBase):
    pass

class TrainUpdate(TrainBase):
    pass

class TrainRead(TrainBase):
    id: str
    class Config:
        orm_mode = True

class YardMasterBase(BaseModel):
    name: str
    email: Optional[str] = None

class YardMasterCreate(YardMasterBase):
    pass

class YardMasterUpdate(YardMasterBase):
    pass

class YardMasterRead(YardMasterBase):
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

# --- CRUD Endpoints for Endplate ---

@app.post("/endplates/", response_model=EndplateRead)
def create_endplate(endplate: EndplateCreate, db: Session = Depends(get_db)):
    db_endplate = Endplate(**endplate.dict())
    db.add(db_endplate)
    db.commit()
    db.refresh(db_endplate)
    return db_endplate

@app.get("/endplates/", response_model=List[EndplateRead])
def read_endplates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Endplate).offset(skip).limit(limit).all()

@app.get("/endplates/{endplate_id}", response_model=EndplateRead)
def read_endplate(endplate_id: str, db: Session = Depends(get_db)):
    endplate = db.query(Endplate).filter(Endplate.id == endplate_id).first()
    if not endplate:
        return {"error": "Endplate not found"}
    return endplate

@app.put("/endplates/{endplate_id}", response_model=EndplateRead)
def update_endplate(endplate_id: str, endplate: EndplateUpdate, db: Session = Depends(get_db)):
    db_endplate = db.query(Endplate).filter(Endplate.id == endplate_id).first()
    if not db_endplate:
        return {"error": "Endplate not found"}
    for key, value in endplate.dict().items():
        setattr(db_endplate, key, value)
    db.commit()
    db.refresh(db_endplate)
    return db_endplate

@app.delete("/endplates/{endplate_id}")
def delete_endplate(endplate_id: str, db: Session = Depends(get_db)):
    db_endplate = db.query(Endplate).filter(Endplate.id == endplate_id).first()
    if not db_endplate:
        return {"error": "Endplate not found"}
    db.delete(db_endplate)
    db.commit()
    return {"ok": True}

# --- CRUD Endpoints for Signal ---

@app.post("/signals/", response_model=SignalRead)
def create_signal(signal: SignalCreate, db: Session = Depends(get_db)):
    db_signal = Signal(**signal.dict())
    db.add(db_signal)
    db.commit()
    db.refresh(db_signal)
    return db_signal

@app.get("/signals/", response_model=List[SignalRead])
def read_signals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Signal).offset(skip).limit(limit).all()

@app.get("/signals/{signal_id}", response_model=SignalRead)
def read_signal(signal_id: str, db: Session = Depends(get_db)):
    signal = db.query(Signal).filter(Signal.id == signal_id).first()
    if not signal:
        return {"error": "Signal not found"}
    return signal

@app.put("/signals/{signal_id}", response_model=SignalRead)
def update_signal(signal_id: str, signal: SignalUpdate, db: Session = Depends(get_db)):
    db_signal = db.query(Signal).filter(Signal.id == signal_id).first()
    if not db_signal:
        return {"error": "Signal not found"}
    for key, value in signal.dict().items():
        setattr(db_signal, key, value)
    db.commit()
    db.refresh(db_signal)
    return db_signal

@app.delete("/signals/{signal_id}")
def delete_signal(signal_id: str, db: Session = Depends(get_db)):
    db_signal = db.query(Signal).filter(Signal.id == signal_id).first()
    if not db_signal:
        return {"error": "Signal not found"}
    db.delete(db_signal)
    db.commit()
    return {"ok": True}

# --- CRUD Endpoints for Switch ---

@app.post("/switches/", response_model=SwitchRead)
def create_switch(switch: SwitchCreate, db: Session = Depends(get_db)):
    db_switch = Switch(**switch.dict())
    db.add(db_switch)
    db.commit()
    db.refresh(db_switch)
    return db_switch

@app.get("/switches/", response_model=List[SwitchRead])
def read_switches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Switch).offset(skip).limit(limit).all()

@app.get("/switches/{switch_id}", response_model=SwitchRead)
def read_switch(switch_id: str, db: Session = Depends(get_db)):
    switch = db.query(Switch).filter(Switch.id == switch_id).first()
    if not switch:
        return {"error": "Switch not found"}
    return switch

@app.put("/switches/{switch_id}", response_model=SwitchRead)
def update_switch(switch_id: str, switch: SwitchUpdate, db: Session = Depends(get_db)):
    db_switch = db.query(Switch).filter(Switch.id == switch_id).first()
    if not db_switch:
        return {"error": "Switch not found"}
    for key, value in switch.dict().items():
        setattr(db_switch, key, value)
    db.commit()
    db.refresh(db_switch)
    return db_switch

@app.delete("/switches/{switch_id}")
def delete_switch(switch_id: str, db: Session = Depends(get_db)):
    db_switch = db.query(Switch).filter(Switch.id == switch_id).first()
    if not db_switch:
        return {"error": "Switch not found"}
    db.delete(db_switch)
    db.commit()
    return {"ok": True}

# --- CRUD Endpoints for Block ---

@app.post("/blocks/", response_model=BlockRead)
def create_block(block: BlockCreate, db: Session = Depends(get_db)):
    db_block = Block(**block.dict())
    db.add(db_block)
    db.commit()
    db.refresh(db_block)
    return db_block

@app.get("/blocks/", response_model=List[BlockRead])
def read_blocks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Block).offset(skip).limit(limit).all()

@app.get("/blocks/{block_id}", response_model=BlockRead)
def read_block(block_id: str, db: Session = Depends(get_db)):
    block = db.query(Block).filter(Block.id == block_id).first()
    if not block:
        return {"error": "Block not found"}
    return block

@app.put("/blocks/{block_id}", response_model=BlockRead)
def update_block(block_id: str, block: BlockUpdate, db: Session = Depends(get_db)):
    db_block = db.query(Block).filter(Block.id == block_id).first()
    if not db_block:
        return {"error": "Block not found"}
    for key, value in block.dict().items():
        setattr(db_block, key, value)
    db.commit()
    db.refresh(db_block)
    return db_block

@app.delete("/blocks/{block_id}")
def delete_block(block_id: str, db: Session = Depends(get_db)):
    db_block = db.query(Block).filter(Block.id == block_id).first()
    if not db_block:
        return {"error": "Block not found"}
    db.delete(db_block)
    db.commit()
    return {"ok": True}

# --- CRUD Endpoints for Dispatcher ---

@app.post("/dispatchers/", response_model=DispatcherRead)
def create_dispatcher(dispatcher: DispatcherCreate, db: Session = Depends(get_db)):
    db_dispatcher = Dispatcher(**dispatcher.dict())
    db.add(db_dispatcher)
    db.commit()
    db.refresh(db_dispatcher)
    return db_dispatcher

@app.get("/dispatchers/", response_model=List[DispatcherRead])
def read_dispatchers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Dispatcher).offset(skip).limit(limit).all()

@app.get("/dispatchers/{dispatcher_id}", response_model=DispatcherRead)
def read_dispatcher(dispatcher_id: str, db: Session = Depends(get_db)):
    dispatcher = db.query(Dispatcher).filter(Dispatcher.id == dispatcher_id).first()
    if not dispatcher:
        return {"error": "Dispatcher not found"}
    return dispatcher

@app.put("/dispatchers/{dispatcher_id}", response_model=DispatcherRead)
def update_dispatcher(dispatcher_id: str, dispatcher: DispatcherUpdate, db: Session = Depends(get_db)):
    db_dispatcher = db.query(Dispatcher).filter(Dispatcher.id == dispatcher_id).first()
    if not db_dispatcher:
        return {"error": "Dispatcher not found"}
    for key, value in dispatcher.dict().items():
        setattr(db_dispatcher, key, value)
    db.commit()
    db.refresh(db_dispatcher)
    return db_dispatcher

@app.delete("/dispatchers/{dispatcher_id}")
def delete_dispatcher(dispatcher_id: str, db: Session = Depends(get_db)):
    db_dispatcher = db.query(Dispatcher).filter(Dispatcher.id == dispatcher_id).first()
    if not db_dispatcher:
        return {"error": "Dispatcher not found"}
    db.delete(db_dispatcher)
    db.commit()
    return {"ok": True}

# --- CRUD Endpoints for Train ---

@app.post("/trains/", response_model=TrainRead)
def create_train(train: TrainCreate, db: Session = Depends(get_db)):
    db_train = Train(**train.dict())
    db.add(db_train)
    db.commit()
    db.refresh(db_train)
    return db_train

@app.get("/trains/", response_model=List[TrainRead])
def read_trains(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Train).offset(skip).limit(limit).all()

@app.get("/trains/{train_id}", response_model=TrainRead)
def read_train(train_id: str, db: Session = Depends(get_db)):
    train = db.query(Train).filter(Train.id == train_id).first()
    if not train:
        return {"error": "Train not found"}
    return train

@app.put("/trains/{train_id}", response_model=TrainRead)
def update_train(train_id: str, train: TrainUpdate, db: Session = Depends(get_db)):
    db_train = db.query(Train).filter(Train.id == train_id).first()
    if not db_train:
        return {"error": "Train not found"}
    for key, value in train.dict().items():
        setattr(db_train, key, value)
    db.commit()
    db.refresh(db_train)
    return db_train

@app.delete("/trains/{train_id}")
def delete_train(train_id: str, db: Session = Depends(get_db)):
    db_train = db.query(Train).filter(Train.id == train_id).first()
    if not db_train:
        return {"error": "Train not found"}
    db.delete(db_train)
    db.commit()
    return {"ok": True}

# --- CRUD Endpoints for YardMaster ---

@app.post("/yardmasters/", response_model=YardMasterRead)
def create_yardmaster(yardmaster: YardMasterCreate, db: Session = Depends(get_db)):
    db_yardmaster = YardMaster(**yardmaster.dict())
    db.add(db_yardmaster)
    db.commit()
    db.refresh(db_yardmaster)
    return db_yardmaster

@app.get("/yardmasters/", response_model=List[YardMasterRead])
def read_yardmasters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(YardMaster).offset(skip).limit(limit).all()

@app.get("/yardmasters/{yardmaster_id}", response_model=YardMasterRead)
def read_yardmaster(yardmaster_id: str, db: Session = Depends(get_db)):
    yardmaster = db.query(YardMaster).filter(YardMaster.id == yardmaster_id).first()
    if not yardmaster:
        return {"error": "YardMaster not found"}
    return yardmaster

@app.put("/yardmasters/{yardmaster_id}", response_model=YardMasterRead)
def update_yardmaster(yardmaster_id: str, yardmaster: YardMasterUpdate, db: Session = Depends(get_db)):
    db_yardmaster = db.query(YardMaster).filter(YardMaster.id == yardmaster_id).first()
    if not db_yardmaster:
        return {"error": "YardMaster not found"}
    for key, value in yardmaster.dict().items():
        setattr(db_yardmaster, key, value)
    db.commit()
    db.refresh(db_yardmaster)
    return db_yardmaster

@app.delete("/yardmasters/{yardmaster_id}")
def delete_yardmaster(yardmaster_id: str, db: Session = Depends(get_db)):
    db_yardmaster = db.query(YardMaster).filter(YardMaster.id == yardmaster_id).first()
    if not db_yardmaster:
        return {"error": "YardMaster not found"}
    db.delete(db_yardmaster)
    db.commit()
    return {"ok": True}
