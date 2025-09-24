from fastapi import APIRouter, HTTPException
from app.services.anki_bridge import AnkiBridge
from anki.stats import Stats  # <-- Anki's built-in stats class

router = APIRouter()
bridge = AnkiBridge()

@router.get("/", summary="Get collection stats")
async def stats():
    try:
        return bridge.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_stats(deck_name: str = "All Decks"):
    """
    Returns stats for a deck.
    If no deck_name is passed, returns global stats.
    """
    col = bridge.col
    if deck_name == "All Decks":
        did = 0  # Anki uses deck id 0 for all decks
    else:
        did = col.decks.id(deck_name)

    stats = Stats(col, did, True)
    summary = stats.report()  # returns HTML report normally

    # Instead of HTML, extract structured data
    due_today = col.sched.counts(did)
    total_cards = col.card_count()
    revlog_count = col.db.scalar("select count() from revlog")

    return {
        "deck": deck_name,
        "due_today": {
            "new": due_today[0],
            "learning": due_today[1],
            "review": due_today[2],
        },
        "total_cards": total_cards,
        "total_reviews_logged": revlog_count,
        "report_html": summary,  # keep raw report too if needed
    }




# from fastapi import APIRouter
# from app.services.anki_bridge import AnkiBridge

# router = APIRouter()
# bridge = AnkiBridge()

# @router.get("/")
# async def stats():
#     return {"stats": bridge.get_stats()}
