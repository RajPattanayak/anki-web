# app/models/requests.py
from pydantic import BaseModel
from typing import Optional, Dict

# -------- Decks ---------
class DeckCreateRequests(BaseModel):
    name: str


# -------- Cards ----------
class CardCreateRequest(BaseModel):
    deck_name: str
    front: str
    back: str


# ----------- Study -------------
class StudyAnswerRequest(BaseModel):
    card_id: int
    rating: int # Example: 1=Again, 2=Hard, 3=good, 4+easy 


# ---------- Import ----------
class ImportFileRequest(BaseModel):
    file_type: str # Exmaple: .txt, .csv, .apkg
    options: Optional[Dict] = None