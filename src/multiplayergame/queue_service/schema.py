from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ticketSchema(BaseModel):
    playerID : str
    joinAt : datetime