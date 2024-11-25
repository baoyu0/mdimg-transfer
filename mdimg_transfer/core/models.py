from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from datetime import datetime
from contextlib import asynccontextmanager

Base = declarative_base()

class ProcessingHistory(Base):
    __tablename__ = 'processing_history'
    
    id = Column(Integer, primary_key=True)
    original_url = Column(String(1024), nullable=False)
    processed_url = Column(String(1024))
    file_size_before = Column(Integer)
    file_size_after = Column(Integer)
    mime_type = Column(String(100))
    status = Column(String(50), nullable=False)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    processing_time = Column(Integer)  # 处理时间（毫秒）

async def init_db(database_url: str):
    """初始化数据库"""
    engine = create_async_engine(database_url, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return engine

def get_session_factory(engine) -> async_sessionmaker[AsyncSession]:
    """获取数据库会话工厂"""
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

@asynccontextmanager
async def get_session(session_factory) -> AsyncSession:
    """获取数据库会话的上下文管理器"""
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
