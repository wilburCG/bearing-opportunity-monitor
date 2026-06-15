from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.agent import AgentChatRequest, AgentChatResponse
from app.services.agent import answer_question

router = APIRouter()


@router.post("/chat", response_model=AgentChatResponse)
async def chat(payload: AgentChatRequest, db: Session = Depends(get_db)):
    answer, mode = await answer_question(db, payload.message)
    return AgentChatResponse(answer=answer, mode=mode)
