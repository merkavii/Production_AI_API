# ? Schema مسئول شکل داده است
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class NumPred(BaseModel):
    num: float
    
    
# ? API ما ممکنه پاسخ نامعتبر بده و تضمینی نیست که پاسخش درست باشه.پس یک شما براش درست میکنیم
class PredictionResponse(BaseModel):
    number: float 
    predict: float
    
    
    
class TablePredictionResponse(BaseModel): # @ خروجی به کاربر:
    id: int
    input_text: str
    prediction: str
    confidence: float | None
    model_name: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )# | Pydantic اجازه دارد داده را از attributeهای یک Object بخواند.
    
    
class PredictionCreate(BaseModel): # @ ورودی از کاربر:
    input_text: str
    prediction: str
    confidence: float | None = None
    model_name: str
    
    
    
    
class PredictionUpdate(BaseModel):

    prediction: str | None = None
    confidence: float | None = None
    model_name: str | None = None