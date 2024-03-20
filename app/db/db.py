from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.configs.app_config import app_config

engine = create_async_engine(url=app_config.db_url)
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session
