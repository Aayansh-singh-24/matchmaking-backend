from fastapi import FastAPI
from contextlib import asynccontextmanager
from multiplayergame.config.db import base, engine, mongo_client, mongo_db
from multiplayergame.queue_service.model import _initilize_index


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(base.metadata.create_all)

    await mongo_db.command("ping")
    await _initilize_index()
    
    try:
        yield
    finally:
        await mongo_client.close()
        await engine.dispose()


app = FastAPI(title="Authorized-server", lifespan=lifespan)

@app.get("/")
def home():
    return("Home page  of authorized-server")
