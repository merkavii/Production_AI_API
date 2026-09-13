from sqlalchemy import  text
from app.database import SessionLocal



with SessionLocal() as session:
    result = session.execute(
        text("SELECT current_database(), current_user;")
    )

    row = result.fetchone()

    print("Database:", row[0])
    print("User:", row[1])