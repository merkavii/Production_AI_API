from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app.core.config import settings
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models.user import User
from app.models.prediction import Prediction

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
        
     
# ? وقتی Router این را می‌بیند: db: Session = Depends(get_db)
# ? در حالت عادی می‌رود سراغ DB اصلی.
        
@pytest.fixture
def client(db_session):        
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db # @ هر وقت get_db خواستی  وقت get_db خواستی → از override_get_db استفاده کن
    
    with TestClient(app) as test_client: # | تست اجرا می‌شود بعد کلیر میشود
        yield test_client
    
    app.dependency_overrides.clear()
    
    
@pytest.fixture
def user(db_session):

    user = User(
        name="Ali",
        email="ali@example.com"
    )

    db_session.add(user)
    db_session.flush()

    return user


@pytest.fixture
def prediction(db_session, user):

    prediction = Prediction(
        input_text="schon!",
        prediction="positive",
        confidence=0.79,
        model_name="sentiment-model-v1",
        user_id=user.id
    )

    db_session.add(prediction)
    db_session.flush()

    return prediction