
from sqlalchemy import BigInteger, CheckConstraint, Numeric, Text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.database import Base

class User(Base):
    __tablename__ = 'users'
    
    id : Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement= True,
        
    )
    
    name : Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    
    email : Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True
    )
    
    predictions: Mapped[list["Prediction"]] = relationship(
        back_populates="user"
    )