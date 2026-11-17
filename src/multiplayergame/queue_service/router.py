from fastapi import APIRouter
from multiplayergame.config.db import get_postgres_db
from multiplayergame.queue_service.schema import ticketSchema


router = APIRouter(prefix="/queue", tags=["Queue"])

@router.get("/create_ticket")
def create_ticket(body:ticketSchema):
    pass