
import math
import time

from celery import Celery


# Configuração do Celery com Redis como broker
app = Celery(
    "tarefas_calculo",
    broker="redis://localhost:6379/0",
)

# Configurações do Celery
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Sao_Paulo",
    enable_utc=True,
    task_track_started=True,
    result_expires=3600,
)


@app.task(name="calcular_soma")
def calcular_soma(a: float, b: float):
    """
    Simula um processamento demorado e retorna a soma
    de dois números.
    """
    print(f"Iniciando cálculo da soma: {a} + {b}")

    # Simula uma tarefa que demora 5 segundos
    time.sleep(5)

    resultado = a + b

    print(f"Resultado da soma: {resultado}")

    return {
        "operacao": "soma",
        "a": a,
        "b": b,
        "resultado": resultado,
    }


@app.task(name="calcular_fatorial")
def calcular_fatorial(n: int):
    """
    Simula um processamento demorado e calcula
    o fatorial de um número de forma iterativa.
    """
    print(f"Iniciando cálculo do fatorial de {n}")

    # Simula uma tarefa que demora 5 segundos
    time.sleep(5)

    resultado = math.factorial(n)

    print(f"Resultado do fatorial de {n}: {resultado}")

    return {
        "operacao": "fatorial",
        "numero": n,
        "resultado": resultado,
    }