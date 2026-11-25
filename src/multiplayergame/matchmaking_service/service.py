import logging
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from multiplayergame.queue_service.model import Queue

logger = logging.getLogger(__name__)


class Match:
    """Build a match from the two oldest waiting queue tickets."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.ticket: Sequence[Queue] = ()

    async def fetch_ticket(self) -> Sequence[Queue]:
        result = await self.db.execute(
            select(Queue)
            .where(Queue.matching_status == "waiting")
            .order_by(Queue.joinAT)
            .limit(2)
            .with_for_update(skip_locked=True)
        )
        self.ticket = result.scalars().all()
        return self.ticket

    def is_two_player_exist(self, ticket: Sequence[Queue] | None = None) -> bool:
        """Return whether this ticket contains the two players needed for a match."""
        return len(self.ticket if ticket is None else ticket) >= 2

    async def create(self) -> Sequence[Queue] | None:
        """Return and claim the oldest pair, or None until two players are queued."""
        try:
            await self.fetch_ticket()
            if not self.is_two_player_exist():
                await self.db.rollback()
                logger.info("Matchmaking needs two waiting players; found %d", len(self.ticket))
                return None

            for player in self.ticket:
                player.matching_status = "matched"

            await self.db.commit()
            logger.info(
                "Created match for players %s",
                [player.playerID for player in self.ticket],
            )
            return self.ticket
        except Exception:
            await self.db.rollback()
            logger.exception("Failed to create a matchmaking pair")
            raise
