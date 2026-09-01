from fastapi.testclient import TestClient
from app.main import app, get_model

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    res_json = response.json()
    assert response.status_code == 200
    assert res_json['status'] == 'healthy'
    

def test_predict_endpoint():
    response = client.post(
        '/predict',
        json={
            'num': 10
        }
    )
    res_json = response.json()
    assert response.status_code == 200
    assert res_json['predict'] == 170
    
    

def test_predict_invalid_input():
    response_1 = client.post(
    '/predict',
    json={
        'num': 'hello'
    }
    )
    response_2 = client.post(
    '/predict',
    json={}
    )
    assert response_1.status_code == 422 # ! ببینیم ولیدیشن درست انجام میشه یا نه. انتظار ما 200 نیست
    assert response_2.status_code == 422
    
    
def test_predict_zero():
    response = client.post(
    '/predict',
    json={
        'num': 0
    }
    )
    assert response.status_code == 400
    
    
def test_get_model():
    response = client.get("/model")

    assert response.status_code == 200
    assert response.json()["model"] == "AI MODEL"
    
 
 
def fake_get_model():
    return "FAKE MODEL"   
def test_model_override():
    # ? Replace the real dependency with a fake one for testing.
    app.dependency_overrides[get_model] = fake_get_model

    response = client.get("/model")

    assert response.status_code == 200
    assert response.json()["model"] == "FAKE MODEL"

    app.dependency_overrides.clear()
    
    
    

def test_async_endpoint():
    response = client.get("/async-test")
    res_json = response.json()
    assert response.status_code == 200
    assert res_json['message'] == "Async works"
    
    
    
def test_background_endpoint():
    response = client.post('/background')
    assert response.status_code == 200
    