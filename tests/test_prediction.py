from app.services.prediction import make_prediction

# | Unit Test: 
# ?make_prediction(10) -> 170 ✅
def test_make_prediction():
    test_value = make_prediction(10)
    assert test_value['predict'] == 170
    
# * python -m pytest