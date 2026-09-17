
from sqlalchemy import select
from app.database import SessionLocal
from app.models.prediction import Prediction


with SessionLocal() as session:
    statement = (
        select(Prediction) # @ SELECT * FROM predictions;
        .where(Prediction.confidence >= 0.80)
        .order_by(Prediction.confidence.desc())
        .limit(2)
    )

    result = session.execute(statement)

    predictions = result.scalars().all() # @ نتیجه را از Rowهای خام دیتابیس به Objectهای Prediction تبدیل می‌کند.

    for item in predictions:
        print(
            item.id,
            item.prediction,
            item.confidence,
        )