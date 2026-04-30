from fastapi import FastAPI
from app.core.config import settings
from app.core.models import AlarmEvent
from app.core.orchestrator import DiagnosisOrchestrator

app = FastAPI(title=settings.app_name, version="1.0.0")
orchestrator = DiagnosisOrchestrator()


@app.get("/")
def healthcheck():
    return {"app": settings.app_name, "status": "ok", "env": settings.app_env}


@app.post("/diagnose")
def diagnose(event: AlarmEvent):
    return orchestrator.run(event)
