
# ? Repository یک لایه مخصوص ارتباط با Data Source است.
# * SELECT
# * INSERT
# * UPDATE
# * DELETE


from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Prediction


class PredictionRepository:

    def __init__(self, db: Session):
        self.db = db


    def get_all(self):
        statement = select(Prediction) # @ SELECT * FROM predictions;

        result = self.db.execute(statement)

        return result.scalars().all()
    
    def get_by_id(self, prediction_id: int):

        statement = select(Prediction).where(
            Prediction.id == prediction_id
        )
        result = self.db.execute(statement)
        return result.scalar_one_or_none()


    def create(self, prediction: Prediction):
        self.db.add(prediction)
        self.db.commit()
        self.db.refresh(prediction)

        return prediction


    def delete(self, prediction: Prediction):
        self.db.delete(prediction)
        self.db.commit()



    def update(self, prediction: Prediction, data: dict):

        for key, value in data.items():
            setattr(
                prediction,
                key,
                value
            )

        self.db.commit()
        self.db.refresh(prediction)

        return prediction
    


