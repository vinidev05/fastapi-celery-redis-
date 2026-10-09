
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from celery_app import calcular_soma, calcular_fatorial


app = FastAPI(
    title="API de Cálculos Assíncronos",
    description=(
        "API que utiliza FastAPI, Celery e Redis "
        "para executar cálculos em segundo plano."
    ),
    version="1.0.0",
)


# Modelo para receber os dados da soma
class SomaRequest(BaseModel):
    a: float
    b: float


# Modelo para receber os dados do fatorial
class FatorialRequest(BaseModel):
    n: int = Field(ge=0, le=10000)


@app.get("/")
def home():
    return {
        "mensagem": "API de Cálculos Assíncronos",
        "status": "online",
        "documentacao": "/docs",
    }


@app.post("/calcular-soma", status_code=202)
def endpoint_calcular_soma(dados: SomaRequest):
    """
    Envia a tarefa de soma para a fila do Celery
    sem esperar o processamento terminar.
    """
    try:
        tarefa = calcular_soma.delay(dados.a, dados.b)

        return {
            "mensagem": "Tarefa de soma enviada para processamento.",
            "task_id": tarefa.id,
            "status": "pendente",
        }

    except Exception as erro:
        raise HTTPException(
            status_code=503,
            detail=f"Não foi possível enviar a tarefa: {str(erro)}",
        )


@app.post("/calcular-fatorial", status_code=202)
def endpoint_calcular_fatorial(dados: FatorialRequest):
    """
    Envia a tarefa de fatorial para a fila do Celery
    sem esperar o processamento terminar.
    """
    try:
        tarefa = calcular_fatorial.delay(dados.n)

        return {
            "mensagem": "Tarefa de fatorial enviada para processamento.",
            "task_id": tarefa.id,
            "status": "pendente",
        }

    except Exception as erro:
        raise HTTPException(
            status_code=503,
            detail=f"Não foi possível enviar a tarefa: {str(erro)}",
        )