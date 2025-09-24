from fastapi import APIRouter, HTTPException
from typing import Optional
from app.models.requests import StudyAnswerRequest
from app.models.responses import StudyAnswerResponse
from app.services.anki_bridge import AnkiBridge

router = APIRouter()
bridge = AnkiBridge()

@router.get("/next", summary="Get the next due card", response_model=dict)
async def get_next(deck_name: Optional[str] = None):
    try:
        result = bridge.get_next_review_card(deck_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/answer", response_model=StudyAnswerResponse, summary="Answer a card and update scheduler")
async def answer_card(req: StudyAnswerRequest):
    try:
        result = bridge.answer_card(req.card_id, req.rating)
        return StudyAnswerResponse(card_id=req.card_id, new_due=result.get("due"), ease_factor=None, status="answered")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# from fastapi import APIRouter

# router = APIRouter()

# @router.post("/answer")
# async def answer_card(card_id: int, rating: int):
#     # integrate with AnkiBridge answer logic later
#     return {"card_id": card_id, "rating": rating, "status": "stub"}
