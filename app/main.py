from fastapi import FastAPI,HTTPException,Depends,BackgroundTasks,UploadFile,Request
import time, uuid
from app.services.file import save_upload_file
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.security import verify_api_key, require_admin
from app.routers import prediction


# * Lifespan
# ? ما برای هر درخواست نمیخوایم مدل رو لود کنیم پس یبار اول برنامه لود و اخر برنامه میبندیمش
# | به طور کل یعنی وقتی برنامه بالا آمد، این کارها را انجام بده. و وقتی برنامه خاموش شد، این کارها را انجام بده.
@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Loading AI model...")

    app.state.model = "AI MODEL" # @ app.state یک محل برای نگه‌داری state مشترک در طول عمر Application است

    yield

    print("Cleaning up AI model...")

    del app.state.model


app = FastAPI(lifespan=lifespan)
app.include_router(
    prediction.router,
    prefix="/prediction", # | توی هرکدوم از اون اندپوینتا بریم قبلش /prediction میزاره
    tags=["Prediction"]
)

# | CORS:
# @ CORS یک محدودیت امنیتی مرورگر است.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # * allow_origins -->  چه Frontendهایی اجازه دارند؟
    allow_credentials=True, # * allow_credentials --→ آیا Cookie / Authentication credentials مجاز است؟ : Credentials یعنی اطلاعات احراز هویت مربوط به Browser : Cookies,some browser authentication ...
    allow_methods=["*"], # * allow_methods --→ چه HTTP methodهایی؟  : GET POST PUT DELETE PATCH --> allow_methods=["GET", "POST"]
    allow_headers=["*"], # * allow_headers --→ چه Headerهایی؟ : HTTP Request می‌تواند Header داشته باشد. : Authorization,Content-Type,X-Request-ID ...
)


def get_model():
    # return "AI MODEL"
    return app.state.model
        

        
@app.get('/hello')
def read_root():
    return {"message": "Hello AI Engineer"}



@app.get('/model')
def getting_model(model= Depends(get_model)): # ? Depends(get_model) : «برای مقدار model، از Dependency به اسم get_model استفاده کن و خودت آن را اجرا کن.»
    # ? # FastAPI خودش Dependency را اجرا کرده و نتیجه را به Endpoint تزریق می‌کند.
    return {'model': model}



        

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
    try:
        return await save_upload_file(file)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
        

# ? یعنی Middleware مثل یک لایه وسط مسیر قرار می‌گیره و می‌تونه روی تمام requestها کاری انجام بده.  
@app.middleware('http')
async def add_process_time(request: Request, call_next): # @ FastAPI وقتی Middleware رو اجرا می‌کنه، خودش دو تا چیز به این تابع می‌ده: request و call_next
    start_time = time.time()
    response = await call_next(request) # | درخواست رو بده به مرحله بعدی؛ وقتی پاسخ برگشت، دوباره کنترل برگرده به Middleware
    # * call_next ---> Request فعلی رو به Middleware/Endpoint بعدی در زنجیره بده و Response اون رو برگردونه.
    process_time = time.time() - start_time
    
    response.headers["X-Process-Time"] = str(process_time)
    return response # ^ حالا وقتی یک اندپوینتو اجرا میکنی توی بخش هدرش میزنه چقدر طول کشید



@app.middleware('http')
async def request_logging(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)
    
    print(
        f"[{request_id}] "
        f"{request.method} {request.url.path} "
        f"→ {response.status_code} "
        f"({process_time:.4f}s)"
    )

    return response



@app.get('/protected')
def protected_route(api_key: str = Depends(verify_api_key)):
    return {"message": "Access granted"}



@app.delete('/model')
def delete_model(user: dict = Depends(require_admin)):
    return {
        "message": "Model deleted",
        "user": user["username"]
    }



# * uvicorn app.main:app --reload