import sqlite3
from typing import List, Optional
from datetime import datetime
from .database import get_connection
from .schemas import MedicoCreate, MedicoUpdate, MedicoResponse

def create_medico(medico: MedicoCreate) -> MedicoResponse:
    """Cria um novo médico"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO medico (nome, especialidade)
            VALUES (?, ?)
        """, (medico.nome, medico.especialidade))
        
        medico_id = cursor.lastrowid
        conn.commit()
        
        # Buscar o médico criado
        cursor.execute("SELECT * FROM medico WHERE id = ?", (medico_id,))
        medico_data = cursor.fetchone()
        
        return MedicoResponse(
            id=medico_data['id'],
            nome=medico_data['nome'],
            especialidade=medico_data['especialidade'],
            created_at=datetime.fromisoformat(medico_data['created_at']),
            updated_at=datetime.fromisoformat(medico_data['updated_at'])
        )

def get_medico_by_id(medico_id: int) -> Optional[MedicoResponse]:
    """Busca médico por ID"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medico WHERE id = ?", (medico_id,))
        medico_data = cursor.fetchone()
        
        if not medico_data:
            return None
            
        return MedicoResponse(
            id=medico_data['id'],
            nome=medico_data['nome'],
            especialidade=medico_data['especialidade'],
            created_at=datetime.fromisoformat(medico_data['created_at']),
            updated_at=datetime.fromisoformat(medico_data['updated_at'])
        )

def get_medicos_by_name(nome: str) -> List[MedicoResponse]:
    """Busca médicos por nome (busca parcial)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM medico 
            WHERE nome LIKE ? 
            ORDER BY nome
        """, (f"%{nome}%",))
        
        medicos_data = cursor.fetchall()
        
        return [
            MedicoResponse(
                id=medico['id'],
                nome=medico['nome'],
                especialidade=medico['especialidade'],
                created_at=datetime.fromisoformat(medico['created_at']),
                updated_at=datetime.fromisoformat(medico['updated_at'])
            )
            for medico in medicos_data
        ]

def get_all_medicos() -> List[MedicoResponse]:
    """Lista todos os médicos"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medico ORDER BY nome")
        medicos_data = cursor.fetchall()
        
        return [
            MedicoResponse(
                id=medico['id'],
                nome=medico['nome'],
                especialidade=medico['especialidade'],
                created_at=datetime.fromisoformat(medico['created_at']),
                updated_at=datetime.fromisoformat(medico['updated_at'])
            )
            for medico in medicos_data
        ]

def update_medico(medico_id: int, medico_update: MedicoUpdate) -> Optional[MedicoResponse]:
    """Atualiza um médico"""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Verificar se o médico existe
        cursor.execute("SELECT * FROM medico WHERE id = ?", (medico_id,))
        if not cursor.fetchone():
            return None
        
        # Construir query de atualização dinamicamente
        update_fields = []
        update_values = []
        
        if medico_update.nome is not None:
            update_fields.append("nome = ?")
            update_values.append(medico_update.nome)
            
        if medico_update.especialidade is not None:
            update_fields.append("especialidade = ?")
            update_values.append(medico_update.especialidade)
        
        if not update_fields:
            return get_medico_by_id(medico_id)
        
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        update_values.append(medico_id)
        
        query = f"UPDATE medico SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, update_values)
        conn.commit()
        
        return get_medico_by_id(medico_id)

def delete_medico(medico_id: int) -> bool:
    """Deleta um médico"""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Verificar se o médico existe
        cursor.execute("SELECT id FROM medico WHERE id = ?", (medico_id,))
        if not cursor.fetchone():
            return False
        
        cursor.execute("DELETE FROM medico WHERE id = ?", (medico_id,))
        conn.commit()
        
        return True 