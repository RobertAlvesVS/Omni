from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base
from app.settings import Configuracoes


engine = create_async_engine(Configuracoes().DATABASE_URL) # type: ignore

async def pegar_sessao():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

Base = declarative_base()