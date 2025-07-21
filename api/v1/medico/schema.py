from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MedicoBase(BaseModel):
    nome: str
    especialidade: str


class MedicoCreate(MedicoBase):
    pass


class MedicoUpdate(BaseModel):
    nome: Optional[str] = None
    especialidade: Optional[str] = None


class MedicoResponse(MedicoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True