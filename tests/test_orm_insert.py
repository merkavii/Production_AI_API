
from app.database import SessionLocal

from app.models import Prediction



with SessionLocal() as session:
    prediction = Prediction(
        input_text="The course was very useful",
        prediction="positive",
        confidence=0.9312,
        model_name="sentiment-model-v1",
    )

    session.add(prediction)
    session.commit()
    
    print("Inserted ID:", prediction.id)