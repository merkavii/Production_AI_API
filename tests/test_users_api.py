from sqlalchemy import select
from app.models.user import User


def test_create_user(client, db_session):
    response = client.post(
        '/user/',
        json={
            "name": "Ali",
            "email": "ali@example.com"
        }
    )
    statement = select(User).where(User.email == "ali@example.com")
    result = db_session.execute(statement).scalar_one_or_none()
    
    assert result is not None
    assert result.name == "Ali"
    assert result.email == "ali@example.com"
    
    data = response.json()
    
    assert response.status_code == 200
    assert data["id"] is not None 
    assert data["name"] == 'Ali'
    assert data["email"] == 'ali@example.com'
    assert result.id == data["id"]
    
   
def test_get_user(client, db_session):
    #| اول user بساز
    # $ اگر Test DB بعد از هر تست rollback می‌شود، در شروع این تست معمولاً
    # $ هیچ Userای تضمین‌شده وجود ندارد. پس باید خود تست یا یک fixture، داده‌ی لازم را بسازد.
    user = User(
        name="Ali",
        email="ali@example.com"
    )

    db_session.add(user)
    db_session.flush()

    response = client.get(f"/user/{user.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == user.id
    assert data["name"] == "Ali"
    assert data["email"] == "ali@example.com"
    
    
def test_get_user_not_found(client):
    response = client.get("/user/999999")

    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "User not found"
    
    
def test_patch_user(client, db_session):
    user = User(
    name="Ali",
    email="ali@example.com"
    )

    db_session.add(user)
    db_session.flush()

    user_id = user.id
    db_session.commit()

    
    response = client.patch(
        f"/user/{user_id}",
        json={
            "name": "Reza"
        }
    )
    data = response.json()
    updated_user = db_session.get(
        User,
        user_id
    )
        
    assert response.status_code == 200
    assert data['id'] == user_id
    assert data["name"] == "Reza"
    assert data["email"] == "ali@example.com"
    assert updated_user.name == 'Reza'
    assert updated_user.email == 'ali@example.com'
    
    
def test_patch_user_not_found(client):
    response = client.patch(
        "/user/999999",
        json={
            "name": "Reza"
        }
    )
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "User not found"
    
    
    
    
def test_delete_user(client, db_session):
    user = User(
    name="Ali",
    email="ali@example.com"
)

    db_session.add(user)
    db_session.flush()

    user_id = user.id
    db_session.commit()

    
    response = client.delete(
        f"/user/{user_id}"
    )
    
    assert response.status_code == 200
    assert response.json() is True
    
    deleted_user = db_session.get(
        User,
        user.id
    )
    assert deleted_user is None