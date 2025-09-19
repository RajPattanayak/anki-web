from fastapi import APIRouter, HTTPException
from app.services.anki_bridge import AnkiBridge
from app.models.requests import DeckCreateRequest

router = APIRouter()
bridge = AnkiBridge()

@router.get("/")
async def list_decks():
    return {"decks": bridge.list_decks()}

@router.post("/")
async def create_deck(payload: DeckCreateRequest):
    result = bridge.create_deck(payload.name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"message": "Deck created successfully", "data": result}