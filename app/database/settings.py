from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv('DB_URL')

class Base(DeclarativeBase):
    pass



engine = create_async_engine(DB_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)





