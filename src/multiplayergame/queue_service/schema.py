from datetime import datetime

from pydantic import BaseModel, Field

class ticketSchema(BaseModel):
    playerID: str = Field(min_length=1, max_length=255)


class ticketCreateResponseSchema(BaseModel):
    playerID: str
    joinAT: datetime
    matching_status: str


class ticketDetailsSchema(BaseModel):
    ticketId: str
    playerId: str
