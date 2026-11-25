from sqlalchemy import Column, Integer,String,DateTime, Boolean
from multiplayergame.config.db import base
from datetime import datetime, timezone

class Queue(base):
    __tablename__ = "matchmaking"
    id : int = Column(Integer, primary_key=True, unique=True,nullable=False)
    playerID : str = Column(String, unique=True, nullable=False)
    ticketID : str = Column(String, unique=True, nullable=False)
    playerStatus : bool = Column(Boolean, nullable=False)
    joinAT : datetime = Column(DateTime(timezone=True), index=True , default=lambda:datetime.now(timezone.utc), nullable=True)
    matching_status: str = Column(String, nullable=False, default="waiting")
