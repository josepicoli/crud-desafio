from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List
from api.v1.medico.schema import MedicoResponse, MedicoCreate, MedicoUpdate
from api.v1.medico.service import medico_service as service
from api.utils.exceptions import ExceptionInternalErro, ExceptionNotFound
from api.utils.db_utils import get_db

router = APIRouter(prefix="/medicos", tags=["médicos"])

NOT_FOUND = "medico não encontrado"

@router.post("/", response_model=MedicoResponse, status_code=201)
def criar_medico(medico: MedicoCreate, db: Session = Depends(get_db)):
    """Cria um novo médico"""
    try:
        return service.create_medico(db=db, medico=medico)
    except Exception as e:
        raise ExceptionInternalErro(detail=f"Erro ao criar médico: {str(e)}")

@router.get("/", response_model=List[MedicoResponse])
def listar_medicos(nome: str = Query(None, description="Buscar médicos por nome"), db: Session = Depends(get_db)):
    """Lista todos os médicos ou busca por nome"""
    try:
        if nome:
            return service.get_medicos_by_name(db, nome)
        return service.get_medicos(db)
    except Exception as e:
        raise ExceptionInternalErro(detail=f"Erro ao buscar médicos: {str(e)}")

@router.get("/{medico_id}", response_model=MedicoResponse)
def buscar_medico_por_id(medico_id: int, db: Session = Depends(get_db)):
    """Busca um médico por ID"""
    try:
        medico = service.get_medico(db, medico_id)
        if not medico:
            raise ExceptionNotFound(detail="Médico não encontrado")
        return medico
    
    except Exception as e:
        raise ExceptionInternalErro(detail=f"Erro ao buscar médico: {str(e)}")

@router.put("/{medico_id}", response_model=MedicoResponse)
def atualizar_medico(medico_id: int, medico_update: MedicoUpdate, db: Session = Depends(get_db)):
    """Atualiza um médico"""
    try:
        medico = service.update_medico(db, medico_id, medico_update)
        if not medico:
            raise ExceptionNotFound(detail="Médico não encontrado")
        return medico
    
    except Exception as e:
        raise ExceptionInternalErro(detail=f"Erro ao atualizar médico: {str(e)}")

@router.delete("/{medico_id}")
def deletar_medico(medico_id: int, db: Session = Depends(get_db)):
    """Deleta um médico"""
    try:
        success = service.delete_medico(db, medico_id)
        if not success:
            raise ExceptionNotFound(detail="Médico não encontrado: ")
        return {"message": "Médico deletado com sucesso"}
    
    except Exception as e:
        raise ExceptionInternalErro(detail=f"Erro ao excluir: {str(e)}")