from fastapi import APIRouter
from app.services.anki_bridge import AnkiBridge

router = APIRouter()
bridge = AnkiBridge()

@router.post("/answer")
async def answer_card(card_id: int, rating: int):
    """
    rating: 1=Again, 2=Hard, 3=Good, 4=Easy
    """
    col = bridge.col
    card = col.get_card(card_id)

    # Call into Anki's scheduler
    col.sched.answer_card(card, rating)

    col.save()
    return {
        "card_id": card_id,
        "rating": rating,
        "new_interval": card.ivl,   # interval in days
        "ease_factor": card.factor / 1000.0,  # ease factor
        "due": card.due,
        "type": card.type
    }



# from fastapi import APIRouter

# router = APIRouter()

# @router.post("/answer")
# async def answer_card(card_id: int, rating: int):
#     # integrate with AnkiBridge answer logic later
#     return {"card_id": card_id, "rating": rating, "status": "stub"}
