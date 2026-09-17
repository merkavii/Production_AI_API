from app.repositories.user import UserRepository
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.exceptions import UserNotFound

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
        self.db = db
        
    def get_all_users(self):
        return self.repository.get_all()
    
    def get_user(self, user_id):
        user = self.repository.get_by_id(user_id)
        
        if user is None:
            raise UserNotFound()
        return user
    
    def create_user(self, data):
        with self.db.begin():
            user_obj = User(
                name=data.name,
                email=data.email
            )

            user = self.repository.create(user_obj)

            self.db.refresh(user)

        return user
    
    def update_user(
        self,
        user_id: int,
        data
        ):
        with self.db.begin():
            user = self.repository.get_by_id(
                user_id
            )

            if user is None:
                raise UserNotFound()

            user =  self.repository.update(
                user,
                data.model_dump(
                    exclude_unset=True
                )
            )
            self.db.refresh(user)
            
            return user
        
        
    def delete_user(
        self,
        user_id: int
    ):
        with self.db.begin():

            user = self.repository.get_by_id(
                user_id
            )

            if user is None:
                raise UserNotFound()
            
            self.repository.delete(user)

            return True
        