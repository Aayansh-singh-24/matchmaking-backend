import secrets
import string
import logging

from datetime import datetime
from multiplayergame.config.db import get_mongo_db
from sqlalchemy.ext.asyncio import AsyncSession
from multiplayergame.queue_service.model import Queue

logger = logging.getLogger(__name__)

class playerTicket:
    def __init__(self, playerId:str, joinAT:datetime, ):
        self.playerId  = playerId
        self.joinAT  = joinAT

    def _generate_ticket_id(self) -> str:
        alphabet = string.ascii_uppercase + string.digits
        ticket_id = ''.join(secrets.choice(alphabet) for _ in range(10))
        return ticket_id


    async def create_ticket(self,db:AsyncSession) -> None:
        ticketId = self._generate_ticket_id()
        ticket = Queue(
            playerID = self.playerId,
            ticketID = ticketId,
            playerStatus = True,
            joinAT = self.joinAT,
        )

        try:
            db.add(ticket)
            await db.commit()
            await db.refresh(ticket)

        except Exception:
            logger.exception("Failed to add queue ticket for player %s", self.playerId)
            raise

        logger.info("Added queue ticket to the database session for player %s", self.playerId)
