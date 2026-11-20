import logging

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker,create_async_engine
from multiplayergame.config.setting import setting
from sqlalchemy.orm import declarative_base

from pymongo import AsyncMongoClient

logger = logging.getLogger(__name__)

# postgres connection Implementation
engine = create_async_engine(setting.POSTGRES_DATABASE_URL, echo=False, connect_args={"timeout": 10})
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, autocommit=False, autoflush=False)
base = declarative_base()


async def get_postgres_db():
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            logger.exception("Database session failed; rolling back transaction")
            await session.rollback()
            raise
        finally:
            await session.close()


# mongodb connection Implementation
mongo_client = AsyncMongoClient(setting.MONGODB_DATABASE_URL, TimeoutMS=10000)
mongo_db = mongo_client["player-skills"]

def get_mongo_db():
    return mongo_db


