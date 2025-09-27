from anki.pylib.anki.collection import Collection
from typing import Any, Dict, List, Optional
from pathlib import Path
import threading

ANKI_DB_PATH = Path("./ankiweb_collection.anki2")  # Will the adjust the path
_COLLECTION_LOCK = threading.Lock()

class AnkiBridge:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = Path(db_path) if db_path else ANKI_DB_PATH

    def _open_col(self) -> Collection:
        return Collection(self.db_path)    


    # --- Deck Management ---
    def list_decks(self) -> List[str]:
        with _COLLECTION_LOCK:
            col = self._open_col()
            try:
                return col.decks.all_names()
            finally:
                col.close()

    def create_deck(self, name: str) -> Dict[str, Any]:
        with _COLLECTION_LOCK:
            col = self._open_col()
            try:
                deck_id = col.decks.id(name)
                col.save()
                return {"deck_name": name, "deck_id": deck_id}
            finally:
                col.close()

    def delete_deck(self, deck_name: str) -> Dict[str, Any]:
        with _COLLECTION_LOCK:
            col = self._open_col()
            try:
                deck_id = col.decks.id(deck_name)
                col.decks.rem(deck_id)
                col.save()
                return {"deck": deck_name, "deleted_deck_id": deck_id}
            finally:
                col.close()

    def rename_deck(self, old_name: str, new_name: str) -> Dict[str, Any]:
        with _COLLECTION_LOCK:
            col = self._open_col()
            try:
                deck_id = col.decks.id(old_name)
                col.decks.set_name(deck_id, new_name)
                col.save()
                return {"old": old_name, "new": new_name, "deck_id": deck_id}
            finally:
                col.close()

    def get_deck_config(self, deck_name: str) -> Dict[str, Any]:
        with _COLLECTION_LOCK:
            col = self._open_col()
            try:
                d = col.decks.by_name(deck_name)
                if not d:
                    return {}
                cfg = col.decks.get_config_for_deck(d["id"])
                return {"deck": deck_name, "config": cfg}
            finally:
                col.close()            


    # --- Card Management ---
    def add_card(self, deck_name: str, front: str, back: str) -> Dict[str, Any]:
        with _COLLECTION_LOCK:
            col = self._open_col()
            try:
                deck_id = col.decks.id(deck_name)
                m = col.models.by_name("Basic")
                if m is None:
                    # fallback to any model
                    names = col.models.all_names()
                    first = next(iter(names), None)
                    if first:
                        m = col.models.by_name(first)
                if m is None:
                    raise RuntimeError("No note model available in collection.")

                note = col.new_note(m)
                if len(note.fields) >= 2:
                    note.fields[0] = front
                    note.fields[1] = back
                else:
                    note.fields[0] = f"{front}\n{back}"
                col.add_note(note, deck_id)
                col.save()
                return {"deck": deck_name, "front": front, "back": back, "note_id": getattr(note, "id", None)}
            finally:
                col.close()
        

    def list_cards(self, deck_name: str) -> Dict[str, Any]:
        with _COLLECTION_LOCK:
            col = self._open_col()
            try:
                # returns card ids
                card_ids = col.find_cards(f"deck:{deck_name}")
                cards = []
                for cid in card_ids:
                    try:
                        c = col.get_card(cid)
                        cards.append(
                            {
                                "id": cid,
                                "deck": deck_name,
                                "due": getattr(c, "due", None),
                                "interval": getattr(c, "ivl", None) or getattr(c, "interval", None),
                                "type": getattr(c, "type", None),
                                "flags": getattr(c, "flags", None),
                            }
                        )
                    except Exception:
                        pass
                return {"deck": deck_name, "cards": cards}
            finally:
                col.close()

    def edit_card(self, card_id: int, front: Optional[str], back: Optional[str]) -> Dict[str, Any]:
        with _COLLECTION_LOCK:
            col = self._open_col()
            try:
                card = col.get_card(card_id)
                note = col.get_note(card.nid)
                if front is not None:
                    note.fields[0] = front
                if back is not None:
                    if len(note.fields) > 1:
                        note.fields[1] = back
                col.update_note(note)
                col.save()
                return {"card_id": card_id, "updated": True}
            finally:
                col.close()

    def delete_card(self, card_id: int) -> Dict[str, Any]:
        with _COLLECTION_LOCK:
            col = self._open_col()
            try:
                col.rem_cards([card_id])
                col.save()
                return {"card_id": card_id, "deleted": True}
            finally:
                col.close()

    def suspend_card(self, card_id: int) -> Dict[str, Any]:
        with _COLLECTION_LOCK:
            col = self._open_col()
            try:
                c = col.get_card(card_id)
                c = col.sched.suspend_card(c)
                col.save()
                return {"card_id": card_id, "suspended": True}
            finally:
                col.close()

    def unsuspend_card(self, card_id: int) -> Dict[str, Any]:
        with _COLLECTION_LOCK:
            col = self._open_col()
            try:
                c = col.get_card(card_id)
                c = col.sched.unsuspend_card(c)
                col.save()
                return {"card_id": card_id, "unsuspended": True}
            finally:
                col.close()                
    
    
    # --- Study / Scheduling Management ---
    def get_next_review_card(self, deck_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Simple helper: attempts to fetch the next due card.
        This is a *simple* approach — for production you'd use the same logic as the desktop sched.
        """
        with _COLLECTION_LOCK:
            col = self._open_col()
            try:
                if deck_name:
                    q = f"deck:{deck_name}"
                else:
                    q = ""
                cids = col.find_cards(q + " is:due")
                if not cids:
                    return {"found": False}
                cid = cids[0]
                c = col.get_card(cid)
                return {
                    "found": True,
                    "card": {
                        "id": cid,
                        "nid": getattr(c, "nid", None),
                        "deck": deck_name,
                        "due": getattr(c, "due", None),
                        "interval": getattr(c, "ivl", None) or getattr(c, "interval", None),
                        "question": getattr(c, "question", None) if hasattr(c, "question") else None,
                    },
                }
            finally:
                col.close()

    def answer_card(self, card_id: int, rating: int) -> Dict[str, Any]:
        with _COLLECTION_LOCK:
            col = self._open_col()
            try:
                # Try scheduler's answer API
                try:
                    # newer pylib: col.sched.answer_card(card_id, ease)
                    col.sched.answer_card(card_id, rating)
                except Exception:
                    # fallback: older APIs may exist
                    card = col.get_card(card_id)
                    # some versions expect the CardAnswer proto etc; to keep generic, try this:
                    if hasattr(col, "answer_card"):
                        col.answer_card(card, rating)
                    else:
                        raise RuntimeError("Scheduler answer API not found in installed pylib.")
                col.save()
                # fetch card again
                card = col.get_card(card_id)
                return {
                    "card_id": card_id,
                    "due": getattr(card, "due", None),
                    "interval": getattr(card, "ivl", None) or getattr(card, "interval", None),
                }
            finally:
                col.close()
    

    # --- Stats Management ---
    def get_stats(self) -> Dict[str, Any]:
        with _COLLECTION_LOCK:
            col = self._open_col()
            try:
                try:
                    stats = col.stats()
                    return {"stats": stats}
                except Exception:
                    # fallback minimal
                    decks = col.decks.all_names()
                    return {"decks": decks}
            finally:
                col.close()



# from anki.pylib.collection import Collection
# from pathlib import Path

# ANKI_DB_PATH = Path("./ankiweb_collection.anki2")  # adjust path

# class AnkiBridge:
#     def __init__(self):
#         self.col = Collection(ANKI_DB_PATH)

#     def list_decks(self):
#         return self.col.decks.all_names()

#     def create_deck(self, name: str):
#         return self.col.decks.id(name)

#     def add_card(self, deck_name: str, front: str, back: str):
#         deck_id = self.col.decks.id(deck_name)
#         m = self.col.models.by_name("Basic")
#         note = self.col.new_note(m)
#         note.fields[0] = front
#         note.fields[1] = back
#         self.col.add_note(note, deck_id)
#         self.col.save()
#         return {"deck": deck_name, "front": front, "back": back}
    
#     def get_stats(self):
#         return self.col.stats()
