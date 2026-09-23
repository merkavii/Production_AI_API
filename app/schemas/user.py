from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    name : str
    email : str
    
class UserResponse(BaseModel):
    id : int
    name : str
    email : str
    model_config = ConfigDict(
        from_attributes=True
    )
    
class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None