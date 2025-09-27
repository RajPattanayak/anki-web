from fastapi import APIRouter, HTTPException
from app.services.anki_bridge import AnkiBridge
from app.models.requests import CardCreateRequest
from app.models.responses import CardResponse, CardListResponse

router = APIRouter()
bridge = AnkiBridge()

@router.post("/", response_model=CardResponse, summary="Add a new card")
async def add_card(req: CardCreateRequest):
    result = bridge.add_card(req.deck_name, req.front, req.back)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return CardResponse(deck=result["deck"], front=result["front"], back=result["back"])


@router.get("/{deck_name}", response_model=CardListResponse, summary="List cards in a deck")
async def list_cards(deck_name: str):
    result = bridge.list_cards(deck_name)
    if "deck" not in result:
        raise HTTPException(status_code=400, detail="Unable to list cards")
    return CardListResponse(deck=result["deck"], cards=result["cards"])


@router.put("/{card_id}", summary="Edit an existing card")
async def edit_card(card_id: int, front: str = None, back: str = None):
    try:
        result = bridge.edit_card(card_id, front, back)
        return {"message": "Card updated", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{card_id}", summary="Delete a card")
async def delete_card(card_id: int):
    try:
        result = bridge.delete_card(card_id)
        return {"message": "Card deleted", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{card_id}/suspend", summary="Suspend a card")
async def suspend_card(card_id: int):
    try:
        result = bridge.suspend_card(card_id)
        return {"message": "Card suspended", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{card_id}/unsuspend", summary="Unsuspend a card")
async def unsuspend_card(card_id: int):
    try:
        result = bridge.unsuspend_card(card_id)
        return {"message": "Card unsuspended", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# from fastapi import APIRouter
# from app.services.anki_bridge import AnkiBridge

# router = APIRouter()
# bridge = AnkiBridge()

# @router.post("/")
# async def add_card(deck_name: str, front: str, back: str):
#     result = bridge.add_card(deck_name, front, back)
#     return {"message": "Card added", "card": result}

