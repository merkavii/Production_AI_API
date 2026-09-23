from app.models.user import User
from app.models.prediction import Prediction

def test_create_prediction(client, db_session):

    user = User(
        name="Ali",
        email="ali@example.com"
    )

    db_session.add(user)
    db_session.flush()

    user_id = user.id

    db_session.commit()
    
    response = client.post(
        "/prediction/predictions",
        json={
            "input_text": "This product is great",
            "prediction": "positive",
            "confidence": 0.95,
            "model_name": "sentiment-model-v1",
            "user_id": user_id
        }
    )
    
    data = response.json()
    
    assert response.status_code == 200
    assert data["id"] is not None
    assert data["prediction"] == "positive"
    
    prediction = db_session.get(
        Prediction,
        data["id"]
    )
    assert prediction is not None
    assert prediction.user_id == user_id
    assert prediction.model_name == "sentiment-model-v1"
  
  
    
    
def test_get_prediction(client, db_session):

    user = User(
        name="Ali",
        email="ali@example.com"
    )

    db_session.add(user)
    db_session.flush()
    user_id = user.id

    prediction_1 = Prediction(
        input_text="schon!",
        prediction="positive",
        confidence=0.7912,
        model_name="sentiment-model-v1",
        user_id = user_id
    )
    db_session.add(prediction_1)
    db_session.flush()

    prediction_2 = Prediction(
        input_text="hässlich!",
        prediction="negative",
        confidence=0.93,
        model_name="sentiment-model-v1",
        user_id = user_id
    )
    db_session.add(prediction_2)

    db_session.commit()

    response = client.get(
        '/prediction/predictions'
    )
    data = response.json()
    
    assert response.status_code == 200
    assert len(data) == 2
    for prediction in data:
        assert prediction['id'] is not None
    assert data[0]['prediction'] == 'positive'
    assert data[1]['confidence'] == 0.93
    
    
    
    
def test_get_prediction_by_id(client, db_session):
    user = User(
        name="Ali",
        email="ali@example.com"
    )

    db_session.add(user)
    db_session.flush()
    user_id = user.id

    prediction = Prediction(
        input_text="schon!",
        prediction="positive",
        confidence=0.7912,
        model_name="sentiment-model-v1",
        user_id = user_id
    )
    db_session.add(prediction)
    db_session.flush()
    
    prediction_id = prediction.id
    db_session.commit()
    
    response = client.get(
    f"/prediction/predictions/{prediction_id}"
    )
    data = response.json()
    
    assert response.status_code == 200
    assert data['id'] == prediction_id
    assert data['input_text'] == 'schon!'
    assert data['prediction'] == 'positive'
    


def test_get_prediction_not_found(client):
    response = client.get("/prediction/predictions/999999")

    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "Prediction not found"
    
    
    
def test_patch_prediction(client, db_session):
    user = User(
        name="Ali",
        email="ali@example.com"
    )

    db_session.add(user)
    db_session.flush()
    user_id = user.id
    
    prediction = Prediction(
        input_text="schon!",
        prediction="positive",
        confidence=0.7912,
        model_name="sentiment-model-v1",
        user_id = user_id
    )

    db_session.add(prediction)
    db_session.flush()

    prediction_id = prediction.id
    db_session.commit()

    
    response = client.patch(
        f"/prediction/predictions/{prediction_id}",
        json={
            "input_text": "Außergewöhnlich"
        }
    )
    data = response.json()
    updated_prediction = db_session.get(
        Prediction,
        prediction_id
    )
        
    assert response.status_code == 200
    assert data['id'] == prediction_id
    assert data["input_text"] == "Außergewöhnlich"
    assert data["prediction"] == "positive"
    assert updated_prediction.input_text == 'Außergewöhnlich'
    assert updated_prediction.prediction == 'positive'
    
    
def test_patch_prediction_not_found(client):
    response = client.patch(
        "/prediction/predictions/999999",
        json={
            "input_text": "Außergewöhnlich"
        }
    )
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "Prediction not found"
    
    
    
def test_delete_prediction(client, db_session):
    user = User(
    name="Ali",
    email="ali@example.com"
)

    db_session.add(user)
    db_session.flush()

    user_id = user.id
    
    
    prediction = Prediction(
        input_text="schon!",
        prediction="positive",
        confidence=0.7912,
        model_name="sentiment-model-v1",
        user_id = user_id
    )

    db_session.add(prediction)
    db_session.flush()

    prediction_id = prediction.id
    db_session.commit()


    
    response = client.delete(
        f"/prediction/predictions/{prediction_id}"
    )
    
    assert response.status_code == 200
    assert response.json()["message"] == "Prediction deleted"
    
    deleted_prediction = db_session.get(
        Prediction,
        prediction_id
    )
    assert deleted_prediction is None