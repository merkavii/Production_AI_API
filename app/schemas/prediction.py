# ? Schema مسئول شکل داده است

from pydantic import BaseModel

class NumPred(BaseModel):
    num: float