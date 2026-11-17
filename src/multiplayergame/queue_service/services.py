import secrets
import string

from datetime import datetime
from multiplayergame.config.db import get_mongo_db

class playerTicket:
    def __init__(self, playerId:str, joinAT:datetime, ):
        playerId : str = playerId
        joinAT : datetime = joinAT

    def _generate_ticket_id(self) -> str:
        alphabet = string.ascii_uppercase + string.digits
        ticket_id = ''.join(secrets.choice(alphabet) for _ in range(10))
        return ticket_id

    def ticket() -> None:
        db = get_mongo_db()
        
    
    