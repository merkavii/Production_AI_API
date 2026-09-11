
from fastapi import APIRouter,HTTPException
from app.schemas.prediction import NumPred,PredictionResponse
from app.services.prediction import make_prediction
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