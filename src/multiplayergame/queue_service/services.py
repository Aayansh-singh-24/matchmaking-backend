import secrets
import string
import logging

from sqlalchemy import select
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from multiplayergame.queue_service.model import Queue

logger = logging.getLogger(__name__)

class playerTicket:
    def __init__(self, playerId:str|None , db:AsyncSession):
        self.playerId  = playerId
        self.db = db

    def _generate_ticket_id(self) -> str:
        alphabet = string.ascii_uppercase + string.digits
        ticket_id = ''.join(secrets.choice(alphabet) for _ in range(10))
        return ticket_id

    async def create(self) -> Queue:
        ticketId = self._generate_ticket_id()
        ticket = Queue(
            playerID = self.playerId,
            ticketID = ticketId,
            playerStatus = True,
            joinAT = datetime.now(timezone.utc),
        )

        try:
            self.db.add(ticket)
            await self.db.commit()
            await self.db.refresh(ticket)

        except Exception:
            await self.db.rollback()
            logger.exception("Failed to add queue ticket for player %s", self.playerId)
            raise

        logger.info("Added queue ticket to the database session for player %s", self.playerId)
        return ticket

    async def delete(self) -> None:
        ticket = await self.db.execute(select(Queue).where(Queue.playerID==self.playerId))
        ticket = ticket.scalars().first()
        if ticket is None:
            raise LookupError(f"No queue ticket found for player {self.playerId}")

        try:
            await self.db.delete(ticket)
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            logger.exception("Failed to remove ticket from Queue %s", self.playerId)
            raise

        logger.info("Ticket of %s delete successfully",self.playerId)

    async def get_all_tickets(self) -> list[Queue]:
        result = await self.db.execute(select(Queue))
        return list(result.scalars().all())
