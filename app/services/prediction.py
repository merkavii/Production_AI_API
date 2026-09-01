# service مسئول لاجیک و منطقه

def make_prediction(number: float):
    if number == 0:
        raise ValueError("Cannot predict zero")
    result = number * 17
    return {'number': number,
        'predict' : result}