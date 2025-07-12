from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

# Schemas para Médico
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

# Schemas para Agenda
class AgendaStatus(str, Enum):
    livre = "livre"
    ocupado = "ocupado"

class AgendaBase(BaseModel):
    medico_id: int
    data: datetime
    status: AgendaStatus

class AgendaCreate(AgendaBase):
    pass

class AgendaUpdate(BaseModel):
    medico_id: Optional[int] = None
    data: Optional[datetime] = None
    status: Optional[AgendaStatus] = None

class AgendaResponse(AgendaBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 