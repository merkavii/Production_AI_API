from datetime import datetime


from sqlalchemy import BigInteger, CheckConstraint, Numeric, DateTime, Text, func, ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.database import Base

# ? ORM ابجکت پایتون را تبدیل به اس کیو ال میکنه

class Prediction(Base): # ? یعنی این کلاس یک ORM Model است.همین Base است که کلاس را وارد سیستم ORM SQLAlchemy می‌کند.
    __tablename__ = "predictions"

    #| Base            → این کلاس ORM است
    #@ __tablename__   → به کدام جدول وصل است
    #* mapped_column   → هر attribute به کدام ستون وصل است

    # * یعنی SQLAlchemy انتظار دارد این Attribute در Python یک int باشد.
    id: Mapped[int] = mapped_column( # | می‌گوید این Attribute به یک Column واقعی در Database وصل است.
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )
    # ^ id: Mapped[int] --> این attribute یک فیلد ORM است و مقدار پایتونی آن int خواهد بود.
    
    
    input_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    prediction: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    confidence: Mapped[float | None] = mapped_column(
        Numeric(5, 4),
        nullable=True,
    )

    model_name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    
    processing_time: Mapped[float | None] = mapped_column(
            nullable=True
        )
    
    user_id : Mapped[int | None] = mapped_column(
        ForeignKey('users.id'),
        nullable=True
    )
    
    user: Mapped["User"] = relationship(
    back_populates="predictions"
        )

    __table_args__ = (
        CheckConstraint(
            "confidence >= 0 AND confidence <= 1",
            name="predictions_confidence_range",
        ),
    )
    
    
    
