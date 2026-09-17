from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from typing import Generator


DATABASE_URL = (
    f"postgresql+psycopg://"
    f"production_ai_user:{settings.database_password}"
    "@127.0.0.1:5432/production_ai"
)


engine = create_engine(
    DATABASE_URL,
    pool_size=5, # $ یعنی ۵ Connection دائماً در Pool نگه داشته می‌شود.
    max_overflow=10, # $ یعنی اگر آن ۵ تا مشغول بودند، تا ۱۰ Connection اضافه موقت می‌تواند ساخته شود.
    pool_timeout=30, # $ یعنی اگر همه Connectionها مشغول باشند، Request حداکثر ۳۰ ثانیه صبر می‌کند و بعد خطا می‌دهد
    pool_recycle=1800, # $ یعنی Connectionهای قدیمی بعد از ۳۰ دقیقه recycle شوند؛ برای محیط‌های Cloud مفید است.
    pool_pre_ping=True, # $ یعنی قبل از تحویل Connection، SQLAlchemy یک تست سبک می‌زند تا مطمئن شود Connection مرده نیست.
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()