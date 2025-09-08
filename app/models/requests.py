from pydantic import BaseModel

class CardRequest(BaseModel):
    deck_name: str
    front: str
    back: str
