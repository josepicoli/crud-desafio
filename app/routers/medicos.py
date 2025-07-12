from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/medicos", tags=["médicos"])

@router.post("/", response_model=schemas.MedicoResponse, status_code=201)
def criar_medico(medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
    """Cria um novo médico"""
    try:
        return crud.create_medico(db=db, medico=medico)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar médico: {str(e)}")

@router.get("/", response_model=List[schemas.MedicoResponse])
def listar_medicos(nome: str = Query(None, description="Buscar médicos por nome"), db: Session = Depends(get_db)):
    """Lista todos os médicos ou busca por nome"""
    try:
        if nome:
            return crud.get_medicos_by_name(db, nome)
        return crud.get_medicos(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar médicos: {str(e)}")

@router.get("/{medico_id}", response_model=schemas.MedicoResponse)
def buscar_medico_por_id(medico_id: int, db: Session = Depends(get_db)):
    """Busca um médico por ID"""
    try:
        medico = crud.get_medico(db, medico_id)
        if not medico:
            raise HTTPException(status_code=404, detail="Médico não encontrado")
        return medico
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar médico: {str(e)}")

@router.put("/{medico_id}", response_model=schemas.MedicoResponse)
def atualizar_medico(medico_id: int, medico_update: schemas.MedicoUpdate, db: Session = Depends(get_db)):
    """Atualiza um médico"""
    try:
        medico = crud.update_medico(db, medico_id, medico_update)
        if not medico:
            raise HTTPException(status_code=404, detail="Médico não encontrado")
        return medico
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar médico: {str(e)}")

@router.delete("/{medico_id}")
def deletar_medico(medico_id: int, db: Session = Depends(get_db)):
    """Deleta um médico"""
    try:
        success = crud.delete_medico(db, medico_id)
        if not success:
            raise HTTPException(status_code=404, detail="Médico não encontrado")
        return {"message": "Médico deletado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar médico: {str(e)}") 