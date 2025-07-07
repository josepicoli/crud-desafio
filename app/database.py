import sqlite3
import os
from typing import Optional
from contextlib import contextmanager

DATABASE_PATH = "database.db"

def init_database():
    """Inicializa o banco de dados e cria as tabelas"""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Criar tabela de médicos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                especialidade TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Criar tabela de agenda
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agenda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medico_id INTEGER NOT NULL,
                data DATETIME NOT NULL,
                status TEXT NOT NULL CHECK (status IN ('livre', 'ocupado')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (medico_id) REFERENCES medico (id)
            )
        """)
        
        conn.commit()

@contextmanager
def get_connection():
    """Context manager para conexões com o banco"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Permite acesso por nome de coluna
    try:
        yield conn
    finally:
        conn.close()

 