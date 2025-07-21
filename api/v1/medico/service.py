from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime
from api.v1.medico.schema import MedicoCreate, MedicoUpdate
from api.v1._database.models import Medico

class MedicoService:
    
    def create_medico(self, db: Session, medico: MedicoCreate) -> Medico:
        db_medico = Medico(**medico.model_dump())
        db.add(db_medico)
        db.commit()
        db.refresh(db_medico)
        return db_medico

    def get_medico(self, db: Session, medico_id: int) -> Optional[Medico]:
        return db.query(Medico).filter(Medico.id == medico_id).first()

    def get_medicos(self, db: Session, skip: int = 0, limit: int = 100) -> List[Medico]:
        return db.query(Medico).offset(skip).limit(limit).all()

    def get_medicos_by_name(self, db: Session, nome: str) -> List[Medico]:
        """Busca médicos por nome (busca parcial)"""
        return db.query(Medico).filter(
            Medico.nome.ilike(f"%{nome}%")
        ).order_by(Medico.nome).all()

    def update_medico(self, db: Session, medico_id: int, medico: MedicoUpdate) -> Optional[Medico]:
        db_medico = self.get_medico(db, medico_id)
        if not db_medico:
            return None
        
        update_data = medico.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_medico, field, value)
        
        db.commit()
        db.refresh(db_medico)
        return db_medico

    def delete_medico(self, db: Session, medico_id: int) -> bool:
        db_medico = self.get_medico(db, medico_id)
        if not db_medico:
            return False
        
        db.delete(db_medico)
        db.commit()
        return True

medico_service = MedicoService()