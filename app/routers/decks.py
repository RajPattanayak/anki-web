from fastapi import APIRouter
from app.services.anki_bridge import AnkiBridge

router = APIRouter()
bridge = AnkiBridge()

@router.get("/")
async def list_decks():
    return {"decks": bridge.list_decks()}

@router.post("/")
async def create_deck(name: str):
    deck_id = bridge.create_deck(name)
    return {"message": f"Deck '{name}' created", "deck_id": deck_id}
