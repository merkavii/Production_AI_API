from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app.core.config import settings


test_engine = create_engine(
    settings.test_database_url
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)


@pytest.fixture
def db_session():
    connection = test_engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(
        bind=connection
    )

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()