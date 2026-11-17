import logging

from sqlalchemy import Column, Integer,String,DateTime, Boolean
from multiplayergame.config.db import base, get_mongo_db
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class Queue(base):
    __tablename__ = "matchmaking"
    id : int = Column(Integer, primary_key=True, unique=True,nullable=False)
    playerID : str = Column(String, unique=True, nullable=False)
    ticketID : str = Column(String, unique=True, nullable=False)
    playerStatus : bool = Column(Boolean, nullable=False)
    joinAT : datetime = Column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc), nullable=True)
    matching_status: str = Column(String, nullable=False, default="waiting")


async def _initilize_index() -> None:

    db = get_mongo_db()
    
    try:
        await db.Queue.create_index("playerID", unique=True)
    except Exception:
        logger.exception("Failed to create the MongoDB playerID index")
        raise
    logger.info("Ensured MongoDB playerID index exists")
