from fastapi import FastAPI,HTTPException,Depends,BackgroundTasks,UploadFile
import torch, tensorflow, sklearn
from app.schemas.prediction import NumPred,PredictionResponse
from app.services.prediction import make_prediction


app = FastAPI()


def get_model():
    return "AI MODEL"
        

        
@app.get('/hello')
def read_root():
    return {"message": "Hello AI Engineer"}

@app.get('/health')
def check_health():
    return {'status': 'healthy'}

@app.get('/model')
def getting_model(model= Depends(get_model)): # ? Depends(get_model) : «برای مقدار model، از Dependency به اسم get_model استفاده کن و خودت آن را اجرا کن.»
    # ? # FastAPI خودش Dependency را اجرا کرده و نتیجه را به Endpoint تزریق می‌کند.
    return {'model': model}


@app.post('/predict',
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
        

@app.get('/async-test')
async def async_function(): # @ While waiting, the event loop can handle other requests.
    return {"message": "Async works"}

# ? تسک رو میزاریم در بکگرتند انجام بشه ولی ریسپانس ب کلاینت برمیگردونیم اما برای کار خیلی سنگین مثل ترین کردن نیست
@app.post('/background')
def process(background_tasks: BackgroundTasks): # @ پارامتر background_tasks باید یک شیء از نوع BackgroundTasks باشد.
    background_tasks.add_task(print, "Background task executed")
    return {"status": "processing"}



@app.post("/upload")
async def upload_file(file: UploadFile):
    return {
        "filename": file.filename,
        "content_type": file.content_type
    }

# * uvicorn main:app --reload