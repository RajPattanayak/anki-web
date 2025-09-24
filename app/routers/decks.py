from fastapi import APIRouter, HTTPException
from app.services.anki_bridge import AnkiBridge
from app.models.requests import DeckCreateRequest
from app.models.responses import DeckResponse

router = APIRouter()
bridge = AnkiBridge()

@router.get("/", response_model=DeckResponse, summary="List all decks")
async def list_decks():
    decks = bridge.list_decks()
    return DeckResponse(decks=decks)


@router.get("/tree", summary="Get decks in a tree structure")
async def list_deck_tree():
    """
    Returns decks as a tree so frontend can render nested structure.
    Example output:
    [
        {"name": "Math", "children": [
            {"name": "Math::Algebra", "children": []}
        ]}
    ]
    """
    decks = bridge.list_decks()
    tree = {}
    for d in decks:
        parts = d.split("::")
        current = tree
        for p in parts:
            if p not in current:
                current[p] = {"children": {}}
            current = current[p]["children"]

    def to_list(node, prefix=""):
        result = []
        for name, val in node.items():
            full_name = f"{prefix}::{name}" if prefix else name
            result.append({
                "name": full_name,
                "children": to_list(val["children"], full_name)
            })
        return result

    return {"decks": to_list(tree)}


@router.post("/", summary="Create a new deck")
async def create_deck(req: DeckCreateRequest):
    try:
        result = bridge.create_deck(req.name)
        return {"message": "Deck created", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.delete("/{deck_name}", summary="Delete a deck")
async def delete_deck(deck_name: str):
    try:
        result = bridge.delete_deck(deck_name)
        return {"message": "Deck deleted", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.put("/{deck_name}/rename", summary="Rename a deck")
async def rename_deck(deck_name: str, new_name: str):
    try:
        result = bridge.rename_deck(deck_name, new_name)
        return {"message": "Deck renamed", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/{deck_name}/config", summary="Get deck configuration")
async def get_deck_config(deck_name: str):
    try:
        result = bridge.get_deck_config(deck_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))    