from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker,create_async_engine
from multiplayergame.config.setting import setting
from sqlalchemy.orm import declarative_base

engine = create_async_engine(setting.DATABASE_URL, echo=False,)
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, autocommit=False, autoflush=False)
base = declarative_base()


async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            session.close()
