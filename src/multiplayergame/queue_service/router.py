from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from multiplayergame.config.db import get_postgres_db
from multiplayergame.queue_service.controller import create
from multiplayergame.queue_service.schema import ticketSchema, ticketCreateResponseSchema


router = APIRouter(prefix="/queue", tags=["Queue"])

@router.post("/create_ticket", response_model=ticketCreateResponseSchema, status_code=201)
async def create_ticket(body: ticketSchema, db: AsyncSession = Depends(get_postgres_db)) -> ticketCreateResponseSchema:
    return await create(body, db)
