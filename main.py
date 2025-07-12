from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import create_tables
from app.routers import medicos
from app.routers import agenda

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Criar tabelas na inicialização
    create_tables()
    yield

app = FastAPI(
    title="Agenda Médica API",
    description="API para gerenciamento de agenda médica",
    version="1.0.0",
    lifespan=lifespan
)

# Incluir routers
app.include_router(medicos.router)
app.include_router(agenda.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Agenda Médica"} 