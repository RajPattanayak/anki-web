from anki.pylib.collection import Collection
from pathlib import Path

ANKI_DB_PATH = Path("./ankiweb_collection.anki2")  # adjust path

class AnkiBridge:
    def __init__(self):
        self.col = Collection(ANKI_DB_PATH)

    def list_decks(self):
        return self.col.decks.all_names()

    def create_deck(self, name: str):
        return self.col.decks.id(name)

    def add_card(self, deck_name: str, front: str, back: str):
        deck_id = self.col.decks.id(deck_name)
        m = self.col.models.by_name("Basic")
        note = self.col.new_note(m)
        note.fields[0] = front
        note.fields[1] = back
        self.col.add_note(note, deck_id)
        self.col.save()
        return {"deck": deck_name, "front": front, "back": back}
    
    def get_stats(self):
        return self.col.stats()
