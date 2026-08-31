from fastapi import FastAPI
import torch, tensorflow, sklearn
from schemas.prediction import NumPred
from services.prediction import make_prediction

app = FastAPI()

# @app.post('/predict')
# def predict(model, input, model_type):
#     if model_type == torch.nn or model_type == 'torch':
#         model.eval()
#         with torch.inference_mode():    
#             prediction = model(input)
#         return {'prediction': prediction}
#     if model_type == tensorflow.keras.Model or model_type == 'tensorflow':
#         prediction = model.predict(input)
#         return {'prediction': prediction}
    
#     if model_type == 'sklearn' or model_type == sklearn.base.ClassifierMixin or model_type == sklearn.base.RegressorMixin :
#         prediction = model.predict(input)
#         return {'prediction': prediction}
        
@app.get('/hello')
def read_root():
    return {"message": "Hello AI Engineer"}

@app.get('/health')
def check_health():
    return {'status': 'healthy'}



@app.post('/predict')
def predict(number: NumPred):
    x = number.num
    result = make_prediction(number= x)
    return result




# * uvicorn main:app --reload