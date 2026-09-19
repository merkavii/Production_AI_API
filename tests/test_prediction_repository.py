from app.models.prediction import Prediction
from app.repositories.prediction import PredictionRepository


def test_create_prediction(db_session):
    repo = PredictionRepository(db_session)

    prediction = Prediction(
        input_text="Gut und billig",
        prediction="positive",
        confidence=0.8312,
        model_name="sentiment-model-v1",
    )

    created = repo.create(prediction)

    assert created.id is not None
    assert created.prediction == "positive"