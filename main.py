from fastapi import FastAPI
from app.routers import decks, cards, study, stats, users

app = FastAPI(title="Anki Web API", version="0.1")

# Include routers
app.include_router(decks.router, prefix="/decks", tags=["Decks"])
app.include_router(cards.router, prefix="/cards", tags=["Cards"])
app.include_router(study.router, prefix="/study", tags=["Study"])
app.include_router(stats.router, prefix="/stats", tags=["Stats"])
app.include_router(users.router, prefix="/users", tags=["Users"])

# @app.get("/")
# async def root():
#     return {"message": "Welcome to Anki Web API"}

@app.get("/")
async def root():
    return {
        "message": "Welcome to Anki Web API",
        "routes": [
            "/decks",
            "/cards",
            "/study",
            "/stats",
            "/users",
        ],
    }