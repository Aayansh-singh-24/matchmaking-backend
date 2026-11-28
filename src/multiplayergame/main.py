import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from multiplayergame.config.db import base, engine, mongo_client, mongo_db
from multiplayergame.queue_service.router import router as queue_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Match-Making Server")
    try:
        async with engine.begin() as connection:
            await connection.run_sync(base.metadata.create_all)

        logger.info("PostgreSQL schema is ready")

        await mongo_db.command("ping")
        logger.info("MongoDB connection is ready")

    except Exception:
        logger.exception("Application startup failed")
        raise
    
    try:
        yield
    finally:
        logger.info("Shutting down Authorized-server")

        await mongo_client.close()
        await engine.dispose()
        
        logger.info("Database clients closed")


app = FastAPI(title="Authorized-server", lifespan=lifespan)
app.include_router(queue_router)

@app.get("/")
def home():
    return("Home page  of matchmaking service")
