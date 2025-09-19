from anki.pylib.anki.collection import Collection
from pathlib import Path

ANKI_DB_PATH = Path("./ankiweb_collection.anki2")  # Will the adjust the path later

class AnkiBridge:
    def __init__(self):
        self.col = Collection(ANKI_DB_PATH)


    # --- Deck Management ---
    def list_decks(self):
        return self.col.decks.all_names()

    def create_deck(self, name: str):
        try:
            deck_id = self.col.decks.id(name)
            self.col.save()
            return {"deck_name": name, "deck_id": deck_id}
        except Exception as e:
            return {"error": str(e)}


    # --- Card Management ---
    def add_card(self, deck_name: str, front: str, back: str):
        try:
            deck_id = self.col.decks.id(deck_name)
            m = self.col.models.by_name("Basic")
            note = self.col.new_note(m)
            note.fields[0] = front
            note.fields[1] = back
            self.col.add_note(note, deck_id)
            self.col.save()
            return {"deck": deck_name, "front": front, "back": back}
        except Exception as e:
            return {"error": str(e)}
        

    def list_cards(self, deck_name: str):
        try:
            deck_id = self.col.decks.id(deck_name)
            cards = self.col.find_cards(f"deck:{deck_name}")
            return {"deck": deck_id, "cards": cards}
        except Exception as e:
            return {"error": str(e)}    
    
    def get_stats(self):
        return self.col.stats()


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
