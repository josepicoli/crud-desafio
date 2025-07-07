from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_database
from app.routers import medicos

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Inicializar banco de dados na inicialização
    init_database()
    yield

app = FastAPI(
    title="Agenda Médica API",
    description="API para gerenciamento de agenda médica",
    version="1.0.0",
    lifespan=lifespan
)

# Incluir routers
app.include_router(medicos.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Agenda Médica"} 