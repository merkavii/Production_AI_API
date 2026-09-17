from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService
from app.repositories.user import UserRepository

router = APIRouter()

@router.post('/',
            response_model= UserResponse)
def create_user(data: UserCreate,
    db: Session = Depends(get_db)):
    service = UserService(db)
    return service.create_user(data) 


@router.get('/{user_id}',
            response_model=UserResponse)
def get_user(user_id:int,
             db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_user(user_id)