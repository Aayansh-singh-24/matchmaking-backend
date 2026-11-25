import logging

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from multiplayergame.queue_service.services import playerTicket
from multiplayergame.queue_service.schema import ticketSchema, ticketCreateResponseSchema
from multiplayergame.matchmaking_service.service import Match

logger = logging.getLogger(__name__)


async def create(body:ticketSchema ,db:AsyncSession) -> ticketCreateResponseSchema:
    
    player = playerTicket(playerId=body.playerID, db=db)
    try:
        ticket = await player.create()
    except IntegrityError as exc:
        logger.exception("Ticket is not generated %s", body.playerID)
        raise HTTPException(status_code=409, detail="A queue ticket already exists for this player or ticket ID.") from exc

    

    logger.info("Created queue ticket for player %s", body.playerID)
    try:
        match = await Match(db).create()
        if match is not None:
            logger.info("Matched queue ticket for players %s", [item.playerID for item in match])
    except Exception as exc:
        # Keep the successfully-created queue ticket; a later join can retry matching.
        logger.exception("Matchmaking failed after creating ticket for player %s", body.playerID)
        raise HTTPException(status_code=500, detail="Queue ticket created, but matchmaking failed.") from exc

    return ticketCreateResponseSchema(
        playerID=ticket.playerID,
        joinAT=ticket.joinAT,
        matching_status=ticket.matching_status,
    )

async def cancel(id:str, db:AsyncSession):
    player = playerTicket(playerId=id,db=db)
    try:
        await player.delete()
    except LookupError:
        raise HTTPException(status_code=404, detail="Queue ticket not found.")
    
    except Exception as exc:
        logger.exception("Failed to cancel queue ticket for player %s", id)
        raise HTTPException(status_code=500, detail="Failed to cancel queue ticket.") from exc

    logger.info("Cancelled queue ticket for player %s", id)
    return {"detail": "Queue ticket cancelled successfully."}
