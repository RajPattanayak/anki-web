from pydantic import BaseModel
from typing import List

class DeckResponse(BaseModel):
    decks: List[str]

class CardResponse(BaseModel):
    deck: str
    front: str
    back: str
