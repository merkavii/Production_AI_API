from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models.prediction import Prediction
from app.schemas.prediction import NumPred,PredictionResponse,PredictionCreate, TablePredictionResponse, PredictionUpdate
from app.services.prediction import make_prediction, PredictionService
from app.repositories.prediction import PredictionRepository
router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}



@router.post('/predict',
          response_model= PredictionResponse) # @ خروجی این Endpoint باید مطابق PredictionResponse باشد.
def predict(number: NumPred):
    try:
        x = number.num
        result = make_prediction(number= x)
        return result
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Cannot predict zero"
        )
        
        
@router.get("/predictions",
            response_model= list[TablePredictionResponse])
def get_predictions(
    db: Session = Depends(get_db)
):
    service = PredictionService(db)
    predictions = service.get_predictions()
    return predictions



@router.get(
    "/predictions/{prediction_id}",
    response_model=TablePredictionResponse
)
def get_prediction_by_id(
    prediction_id:int,
    db: Session = Depends(get_db)
):
    service = PredictionService(db)
    prediction = service.get_prediction(prediction_id)
    return prediction



@router.post(
    "/predictions",
    response_model=TablePredictionResponse
)
def create_prediction(
    data: PredictionCreate,
    db: Session = Depends(get_db)
):
    service = PredictionService(db)
    return service.create_prediction(data)



@router.patch(
    "/predictions/{prediction_id}",
    response_model=TablePredictionResponse
)
def update_prediction(
    prediction_id: int,
    data: PredictionUpdate,
    db: Session = Depends(get_db)
):

    service = PredictionService(db)

    return service.update_prediction(
        prediction_id,
        data
    )
    
    
@router.delete(
    "/predictions/{prediction_id}"
)
def delete_prediction(
    prediction_id: int,
    db: Session = Depends(get_db)
):

    service = PredictionService(db)

    service.delete_prediction(
        prediction_id
    )

    return {
        "message": "Prediction deleted"
    }