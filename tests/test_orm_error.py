
from sqlalchemy.exc import SQLAlchemyError
from app.database import SessionLocal

from app.models import Prediction


with SessionLocal() as session:
    try:
        prediction = Prediction(
            input_text="invalid confidence test",
            prediction="positive",
            confidence=1.5000,
            model_name="sentiment-model-v1",
        )

        session.add(prediction)
        session.commit()

        print("Saved successfully")

    except SQLAlchemyError as exc:
        session.rollback()

        print("Database error:")
        print(exc)