from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Medico(Base):
    __tablename__ = "medico"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    especialidade = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamento com agenda
    agendas = relationship("Agenda", back_populates="medico")

class Agenda(Base):
    __tablename__ = "agenda"
    
    id = Column(Integer, primary_key=True, index=True)
    medico_id = Column(Integer, ForeignKey("medico.id"), nullable=False)
    data = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamento com médico
    medico = relationship("Medico", back_populates="agendas")
    
    # Constraint para status
    __table_args__ = (
        CheckConstraint("status IN ('livre', 'ocupado')", name="check_status"),
    ) 