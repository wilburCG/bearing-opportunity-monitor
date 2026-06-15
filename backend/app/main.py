from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.health import router as health_router
from app.api.opportunities import router as opportunities_router
from app.api.opportunity_notes import router as opportunity_notes_router
from app.api.agent import router as agent_router
from app.api.industry import router as industry_router

app = FastAPI(title="行业舆情系统", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, tags=["health"])
app.include_router(opportunities_router, prefix="/api/opportunities", tags=["opportunities"])
app.include_router(opportunity_notes_router, prefix="/api/opportunities", tags=["opportunity-notes"])
app.include_router(agent_router, prefix="/api/agent", tags=["agent"])
app.include_router(industry_router, prefix="/api/industry", tags=["industry"])
app.include_router(industry_router, prefix="/api", tags=["industry-compat"])
