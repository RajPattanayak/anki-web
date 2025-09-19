from fastapi import APIRouter, HTTPException
from app.services.anki_bridge import AnkiBridge
from app.models.requests import CardCreateRequest

router = APIRouter()
bridge = AnkiBridge()

@router.post("/")
async def add_card(payload: CardCreateRequest):
    result = bridge.add_card(payload.deck_name, payload.front, payload.back)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"message": "Card added successfully", "data": result}

@router.get("/{deck_name}")
async def list_cards(deck_name: str):
    result = bridge.list_cards(deck_name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result



# from fastapi import APIRouter
# from app.services.anki_bridge import AnkiBridge

# router = APIRouter()
# bridge = AnkiBridge()

# @router.post("/")
# async def add_card(deck_name: str, front: str, back: str):
#     result = bridge.add_card(deck_name, front, back)
#     return {"message": "Card added", "card": result}

