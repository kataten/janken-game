from fastapi import FastAPI
from app.database import engine, Base
from app.routers import game, auth
from app.models import game as models

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Janken Web App")
app.include_router(game.router)
app.include_router(auth.router)