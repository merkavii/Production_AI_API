# service مسئول لاجیک و منطقه
from app.repositories.prediction import PredictionRepository
from sqlalchemy.orm import Session
from app.models import Prediction


def make_prediction(number: float):
    if number == 0:
        raise ValueError("Cannot predict zero")
    result = number * 17
    return {'number': number,
        'predict' : result}
    
    
class PredictionService:

    def __init__(self, db: Session):
        self.repository = PredictionRepository(db)


    def get_predictions(self):
        return self.repository.get_all()
    
    
    def create_prediction(
        self,
        input_text: str,
        prediction: str,
        confidence: float,
        model_name: str
    ):

        prediction_obj = Prediction(
            input_text=input_text,
            prediction=prediction,
            confidence=confidence,
            model_name=model_name
        )

        return self.repository.create(prediction_obj)  
    
    
    
    def update_prediction(
    self,
    prediction_id: int,
    data
    ):
        prediction = self.repository.get_by_id(
            prediction_id
        )

        if prediction is None:
            raise ValueError(
                "Prediction not found"
            )

        return self.repository.update(
            prediction,
            data.model_dump(
                exclude_unset=True
            )
        )
        
    

    
