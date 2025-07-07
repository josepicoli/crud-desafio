from fastapi import APIRouter, HTTPException, Query
from typing import List
from ..schemas import MedicoCreate, MedicoUpdate, MedicoResponse
from ..crud import (
    create_medico,
    get_medico_by_id,
    get_all_medicos,
    get_medicos_by_name,
    update_medico,
    delete_medico
)

router = APIRouter(prefix="/medicos", tags=["médicos"])

@router.post("/", response_model=MedicoResponse, status_code=201)
def criar_medico(medico: MedicoCreate):
    """Cria um novo médico"""
    try:
        return create_medico(medico)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar médico: {str(e)}")

@router.get("/", response_model=List[MedicoResponse])
def listar_medicos(nome: str = Query(None, description="Buscar médicos por nome")):
    """Lista todos os médicos ou busca por nome"""
    try:
        if nome:
            return get_medicos_by_name(nome)
        return get_all_medicos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar médicos: {str(e)}")

@router.get("/{medico_id}", response_model=MedicoResponse)
def buscar_medico_por_id(medico_id: int):
    """Busca um médico por ID"""
    try:
        medico = get_medico_by_id(medico_id)
        if not medico:
            raise HTTPException(status_code=404, detail="Médico não encontrado")
        return medico
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar médico: {str(e)}")

@router.put("/{medico_id}", response_model=MedicoResponse)
def atualizar_medico(medico_id: int, medico_update: MedicoUpdate):
    """Atualiza um médico"""
    try:
        medico = update_medico(medico_id, medico_update)
        if not medico:
            raise HTTPException(status_code=404, detail="Médico não encontrado")
        return medico
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar médico: {str(e)}")

@router.delete("/{medico_id}")
def deletar_medico(medico_id: int):
    """Deleta um médico"""
    try:
        success = delete_medico(medico_id)
        if not success:
            raise HTTPException(status_code=404, detail="Médico não encontrado")
        return {"message": "Médico deletado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar médico: {str(e)}") 