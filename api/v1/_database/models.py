import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint, UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Medico(BaseModel):
    __tablename__ = "medico"
    
    nome = Column(String, nullable=False)
    especialidade = Column(String, nullable=False)
    
    # Relacionamento com agenda
    agendas = relationship("Agenda", back_populates="medico")

class Agenda(BaseModel):
    __tablename__ = "agenda"
    
    medico_id = Column(UUID, ForeignKey("medico.id"), nullable=False)
    data = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    
    # Relacionamento com médico
    medico = relationship("Medico", back_populates="agendas")
    
    # Constraint para status
    __table_args__ = (
        CheckConstraint("status IN ('livre', 'ocupado')", name="check_status"),
    )
