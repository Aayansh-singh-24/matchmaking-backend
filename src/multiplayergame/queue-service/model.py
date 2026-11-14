from sqlalchemy import Column, Integer,String,DateTime
from multiplayergame.config.db import base
from datetime import datetime, timezone

class Queue(base):
    id : int = Column(Integer, primary_key=True, unique=True,nullable=False)
    playerID : str = Column(String, unique=True, nullable=False)
    ticketID : str = Column(String, unique=True, nullable=False)
    joinAT : datetime = Column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc), nullable=True)
    status: str = Column(String,nullable=False)
    