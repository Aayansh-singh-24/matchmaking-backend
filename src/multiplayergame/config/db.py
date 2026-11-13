from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from multiplayergame.config.setting import setting


engine = create_async_engine(setting.DATABASE_URL, connect_args={"connect_timeout": 5},echo=True)

base = declarative_base()

session = async_sessionmaker(engine=engine,class_=AsyncSession,expire_on_commit=True)

