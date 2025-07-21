from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


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