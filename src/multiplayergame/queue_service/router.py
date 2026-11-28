from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from multiplayergame.config.db import get_postgres_db
from multiplayergame.queue_service import controller
from multiplayergame.queue_service.schema import ticketSchema, ticketCreateResponseSchema, ticketDetailsSchema


router = APIRouter(prefix="/queue", tags=["Queue"])


@router.post("/create_ticket", response_model=ticketCreateResponseSchema, status_code=201)
async def create_ticket(body: ticketSchema, db: AsyncSession = Depends(get_postgres_db)) -> ticketCreateResponseSchema:
    return await controller.create(body, db)

@router.get("/tickets", response_model=list[ticketDetailsSchema])
async def get_tickets(db: AsyncSession = Depends(get_postgres_db)) -> list[ticketDetailsSchema]:
    return await controller.get_tickets(db)

@router.delete("/cancel/{playerID}")
async def cnacel_joining(id:str, db:AsyncSession = Depends(get_postgres_db))->None:
    return await controller.cancel(id,db)
