from fastapi import FastAPI
from contextlib import asynccontextmanager
from multiplayergame.config.db import base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(base.metadata.create_all)
    try:
        yield
    finally:
        await engine.dispose()


app = FastAPI(title="Authorized-server", lifespan=lifespan)

@app.get("/")
def home():
    return("Home page  of authorized-server")
