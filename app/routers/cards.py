from fastapi import APIRouter
from app.services.anki_bridge import AnkiBridge

router = APIRouter()
bridge = AnkiBridge()

@router.post("/")
async def add_card(deck_name: str, front: str, back: str):
    result = bridge.add_card(deck_name, front, back)
    return {"message": "Card added", "card": result}

@router.get("/{deck_name}")
async def list_cards(deck_name: str):
    col = bridge.col
    deck_id = col.decks.id(deck_name)
    cards = col.find_cards(f"deck:{deck_name}")
    return {"deck": deck_name, "cards": cards}




# from fastapi import APIRouter
# from app.services.anki_bridge import AnkiBridge

# router = APIRouter()
# bridge = AnkiBridge()

# @router.post("/")
# async def add_card(deck_name: str, front: str, back: str):
#     result = bridge.add_card(deck_name, front, back)
#     return {"message": "Card added", "card": result}

