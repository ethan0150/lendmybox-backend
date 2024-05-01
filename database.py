from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import getenv

async_engine = create_async_engine(getenv("SQLALCHEMY_DATABASE_URL"))
AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine
)

Base = declarative_base()
async def create_tables():
    async with async_engine.begin() as conn:
        # This will create the tables defined in your models (Base subclasses)
        await conn.run_sync(Base.metadata.create_all)