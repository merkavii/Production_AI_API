from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        statement = select(User)
        result = self.db.execute(statement)
        
        return result.scalars().all()
    
    def get_by_id(self, user_id):
        statement = select(User).where(
            User.id == user_id
        )
        result = self.db.execute(statement)
        
        return result.scalar_one_or_none()
    
    def get_by_email(self, email):
        statement = select(User).where(
            User.email == email
        )
        result = self.db.execute(statement)
        
        return result.scalar_one_or_none()
    
    def create(self, user: User):
        self.db.add(user)
        self.db.flush() 

        return user
    
    def delete(self, user:User):
        self.db.delete(user)
        self.db.flush()
        
        return user
    
    def update(self, user: User, data: dict):

        for key, value in data.items():
            setattr(
                user,
                key,
                value
            )

        self.db.flush()

        return user
    
    def get_by_id_with_predictions(self, user_id):
        statement = (
        select(User)
        .options(selectinload(User.predictions)) # $ User رو بگیر و Predictionهاش رو هم همون موقع آماده کن. |  Predictionهای مرتبط را هم از قبل load کن
        .where(User.id == user_id)
    )
    
        result = self.db.execute(statement)
        
        return result.scalar_one_or_none()
        
    def get_all_with_predictions(self,):
        statement = (
        select(User)
        .options(selectinload(User.predictions)) 
    )
        result = self.db.execute(statement)
        return result.scalars().all()
