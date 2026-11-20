import logging

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from multiplayergame.queue_service.services import playerTicket
from multiplayergame.queue_service.schema import ticketSchema, ticketCreateResponseSchema

logger = logging.getLogger(__name__)


async def create(body:ticketSchema ,db:AsyncSession) -> ticketCreateResponseSchema:
    player = playerTicket(playerId=body.playerID)
    try:
        ticket = await player.create(db)
    except IntegrityError as exc:
        logger.exception("Ticket is not generated %s", body.playerID)
        raise HTTPException(status_code=409, detail="A queue ticket already exists for this player or ticket ID.")


    logger.info("Created queue ticket for player %s", body.playerID)
    return ticketCreateResponseSchema(
        playerID=ticket.playerID,
        joinAT=ticket.joinAT,
        matching_status=ticket.matching_status,
    )
