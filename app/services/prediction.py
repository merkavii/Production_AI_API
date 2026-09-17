# service مسئول لاجیک و منطقه
from app.repositories.prediction import PredictionRepository
from sqlalchemy.orm import Session
from app.models.prediction import Prediction
from app.core.exceptions import PredictionNotFound

def make_prediction(number: float):
    if number == 0:
        raise ValueError("Cannot predict zero")
    result = number * 17
    return {'number': number,
        'predict' : result}
    
    
class PredictionService:

    def __init__(self, db: Session):
        self.repository = PredictionRepository(db)
        self.db = db


    def get_predictions(self):
        return self.repository.get_all()
    
    
    def create_prediction(
        self,data
    ):
        with self.db.begin():

            prediction_obj = Prediction(
                input_text=data.input_text,
                prediction=data.prediction,
                confidence=data.confidence,
                model_name=data.model_name,
                user_id = data.user_id 
            )

            prediction = self.repository.create(prediction_obj)

            self.db.refresh(prediction)
            
            return prediction
        
    def update_prediction(
    self,
    prediction_id: int,
    data
    ):
        with self.db.begin():
            prediction = self.repository.get_by_id(
                prediction_id
            )

            if prediction is None:
                raise PredictionNotFound()

            prediction =  self.repository.update(
                prediction,
                data.model_dump(
                    exclude_unset=True
                )
            )
            self.db.refresh(prediction)
            
            return prediction

        
    
    def delete_prediction(
        self,
        prediction_id: int
    ):
        with self.db.begin():

            prediction = self.repository.get_by_id(
                prediction_id
            )

            if prediction is None:
                raise PredictionNotFound()
            
            self.repository.delete(prediction)


            return True
        

