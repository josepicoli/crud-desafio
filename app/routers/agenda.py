from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/agenda", tags=["Agenda"])

@router.post("/", response_model=schemas.AgendaResponse, status_code=status.HTTP_201_CREATED)
def criar_agenda(agenda: schemas.AgendaCreate, db: Session = Depends(get_db)) -> schemas.AgendaResponse:
    return crud.criar_agenda(db, agenda)

@router.get("/livres/", response_model=List[schemas.AgendaResponse])
def listar_agendas_livres(medico_id: int, data: datetime = Query(..., description="Data no formato YYYY-MM-DD"), db: Session = Depends(get_db)) -> List[schemas.AgendaResponse]:
    return crud.listar_agendas_livres(db, medico_id, data)

@router.get("/ocupadas/", response_model=List[schemas.AgendaResponse])
def listar_agendas_ocupadas(medico_id: int, db: Session = Depends(get_db)) -> List[schemas.AgendaResponse]:
    return crud.listar_agendas_ocupadas(db, medico_id)

@router.post("/{agenda_id}/marcar", status_code=status.HTTP_200_OK)
def marcar_consulta(agenda_id: int, db: Session = Depends(get_db)):
    if not crud.marcar_consulta(db, agenda_id):
        raise HTTPException(status_code=400, detail="Horário não está livre ou não existe.")
    return {"message": "Consulta marcada com sucesso."}

@router.post("/{agenda_id}/cancelar", status_code=status.HTTP_200_OK)
def cancelar_consulta(agenda_id: int, db: Session = Depends(get_db)):
    if not crud.cancelar_consulta(db, agenda_id):
        raise HTTPException(status_code=400, detail="Horário não está ocupado ou não existe.")
    return {"message": "Consulta cancelada com sucesso."}

@router.delete("/{agenda_id}", status_code=status.HTTP_200_OK)
def deletar_agenda(agenda_id: int, db: Session = Depends(get_db)):
    if not crud.deletar_agenda(db, agenda_id):
        raise HTTPException(status_code=400, detail="Só é possível deletar horários livres.")
    return {"message": "Agenda deletada com sucesso."}