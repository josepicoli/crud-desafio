from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime

from .v1._database import models
from . import schemas

# CRUD para Agenda
#def create_agenda(db: Session, agenda: schemas.AgendaCreate) -> models.Agenda:
#    db_agenda = models.Agenda(**agenda.model_dump())
#    db.add(db_agenda)
#    db.commit()
#    db.refresh(db_agenda)
#    return db_agenda

def criar_agenda(db: Session, agenda: schemas.AgendaCreate) -> models.Agenda:
    """Cria um novo slot de agenda (status 'livre')"""
    db_agenda = models.Agenda(**agenda.model_dump())
    db.add(db_agenda)
    db.commit()
    db.refresh(db_agenda)
    return db_agenda

def get_agenda(db: Session, agenda_id: int) -> Optional[models.Agenda]:
    return db.query(models.Agenda).filter(models.Agenda.id == agenda_id).first()

#def get_agendas(db: Session, skip: int = 0, limit: int = 100) -> List[models.Agenda]:
#    return db.query(models.Agenda).offset(skip).limit(limit).all()

#def get_agendas_by_medico(db: Session, medico_id: int, skip: int = 0, limit: int = 100) -> List[models.Agenda]:
#    return db.query(models.Agenda).filter(models.Agenda.medico_id == medico_id).offset(skip).limit(limit).all()

#def get_agendas_by_date_range(db: Session, start_date: datetime, end_date: datetime) -> List[models.Agenda]:
#    return db.query(models.Agenda).filter(
#        and_(models.Agenda.data >= start_date, models.Agenda.data <= end_date)
#    ).all()

def listar_agendas_livres(db: Session, medico_id: int, data: datetime) -> List[models.Agenda]:
    """Lista todos os horários livres de um médico em uma data"""
    return db.query(models.Agenda).filter(
        and_(
            models.Agenda.medico_id == medico_id,
            models.Agenda.data >= data.replace(hour=0, minute=0, second=0, microsecond=0),
            models.Agenda.data < data.replace(hour=23, minute=59, second=59, microsecond=999999),
            models.Agenda.status == "livre"
        )
    ).order_by(models.Agenda.data).all()

def listar_agendas_ocupadas(db: Session, medico_id: int) -> List[models.Agenda]:
    """Lista todos os horários ocupados de um médico"""
    return db.query(models.Agenda).filter(
        and_(
            models.Agenda.medico_id == medico_id,
            models.Agenda.status == "ocupado"
        )
    ).order_by(models.Agenda.data).all()

def marcar_consulta(db: Session, agenda_id: int) -> bool:
    """Marca uma consulta (muda status de 'livre' para 'ocupado')"""
    db_agenda = get_agenda(db, agenda_id)
    if not db_agenda or db_agenda.status != "livre":
        return False
    
    db_agenda.status = "ocupado"
    db.commit()
    return True

def cancelar_consulta(db: Session, agenda_id: int) -> bool:
    """Cancela uma consulta (muda status de 'ocupado' para 'livre')"""
    db_agenda = get_agenda(db, agenda_id)
    if not db_agenda or db_agenda.status != "ocupado":
        return False
    
    db_agenda.status = "livre"
    db.commit()
    return True

def deletar_agenda(db: Session, agenda_id: int) -> bool:
    """Deleta um slot da agenda (só se estiver 'livre')"""
    db_agenda = get_agenda(db, agenda_id)
    if not db_agenda or db_agenda.status != "livre":
        return False
    
    db.delete(db_agenda)
    db.commit()
    return True

#def update_agenda(db: Session, agenda_id: int, agenda: schemas.AgendaUpdate) -> Optional[models.Agenda]:
#    db_agenda = get_agenda(db, agenda_id)
#    if not db_agenda:
#        return None
#    
#    update_data = agenda.model_dump(exclude_unset=True)
#    for field, value in update_data.items():
#        setattr(db_agenda, field, value)
#    
#    db.commit()
#    db.refresh(db_agenda)
#    return db_agenda

#def delete_agenda(db: Session, agenda_id: int) -> bool:
#    db_agenda = get_agenda(db, agenda_id)
#    if not db_agenda:
#        return False
#    
#    db.delete(db_agenda)
#    db.commit()
#    return True

#def get_agendas_livres(db: Session, medico_id: Optional[int] = None) -> List[models.Agenda]:
#    query = db.query(models.Agenda).filter(models.Agenda.status == "livre")
#    if medico_id:
#        query = query.filter(models.Agenda.medico_id == medico_id)
#    return query.all()
