from fastapi import FastAPI
from routers import routers

app = FastAPI(
    title="Agenda Médica API",
    description="API para gerenciamento de agenda médica",
    version="1.0.0"
)

app.include_router(routers)

@app.get("/status")
def status():
    return {"message": "api funcionando"}