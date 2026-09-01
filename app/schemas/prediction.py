# ? Schema مسئول شکل داده است

from pydantic import BaseModel

class NumPred(BaseModel):
    num: float
    
    
# ? API ما ممکنه پاسخ نامعتبر بده و تضمینی نیست که پاسخش درست باشه.پس یک شما براش درست میکنیم
class PredictionResponse(BaseModel):
    number: float 
    predict: float