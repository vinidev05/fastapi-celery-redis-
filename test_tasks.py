from celery_app import calcular_soma, calcular_fatorial


def test_calcular_soma():
    resultado = calcular_soma(10, 5)
    assert resultado["resultado"] == 15


def test_calcular_fatorial():
    resultado = calcular_fatorial(5)
    assert resultado["resultado"] == 120


def test_calcular_fatorial_zero():
    resultado = calcular_fatorial(0)
    assert resultado["resultado"] == 1