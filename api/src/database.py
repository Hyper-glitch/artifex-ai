from settings import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_async_engine(settings.postgres_dsn, echo=settings.DEBUG)

async_session_maker = sessionmaker(  # type: ignore
    engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
