# app/models/responses.py
from pydantic import BaseModel
from typing import List, Dict, Optional

# ----- Decks -----
class DeckResponse(BaseModel):
    decks: List[str]

# ----- Cards -----
class CardResponse(BaseModel):
    deck: str
    front: str
    back: str


# Optional: If you want to return a list of cards
class CardListResponse(BaseModel):
    deck: str
    cards: List[Dict]

# ----- Study -----
class StudyAnswerResponse(BaseModel):
    card_id: int
    new_due: Optional[int]
    ease_factor: Optional[float]
    status: str

# ----- Import -----
class ImportResponse(BaseModel):
    success: bool
    imported_count: int
    details: Dict
