from fastapi import APIRouter
from api.v1.medico.controller import router as medicos_router
from api.routers.agenda import router as agenda_router 

routers = APIRouter()
routers.include_router(medicos_router)
routers.include_router(agenda_router)