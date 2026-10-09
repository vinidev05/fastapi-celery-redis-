
# API de Cálculos Assíncronos com FastAPI, Celery e Redis

## 1. Descrição do projeto

Este projeto foi desenvolvido como atividade prática do curso de
Python Back-End da EBAC.

O objetivo é demonstrar como executar tarefas demoradas em segundo
plano utilizando Celery e Redis, integrados a uma API FastAPI.

A aplicação disponibiliza dois endpoints para realizar cálculos:

- Soma de dois números.
- Cálculo do fatorial de um número inteiro.

As tarefas são enviadas para uma fila de processamento e executadas
por um worker Celery separado da API.

Dessa forma, a API pode responder imediatamente após o envio da
tarefa, sem aguardar a conclusão do cálculo.

## 2. Tecnologias utilizadas

- Python
- FastAPI
- Celery
- Redis
- Uvicorn
- Docker e Docker Compose

## 3. Estrutura do projeto

fastapi-celery-redis/
├── celery_app.py
├── main.py
├── requirements.txt
├── docker-compose.yml
├── README.md
└── evidencias/
    └── logs.txt

## 4. Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

- Python 3.10 ou superior.
- Docker Desktop com Docker Compose.
- Visual Studio Code (opcional).

O Docker Desktop deve estar em execução para disponibilizar
o servidor Redis.

## 5. Instalação

### 5.1. Criar o ambiente virtual

Na pasta raiz do projeto, execute:

python -m venv .venv

No Windows PowerShell, ative o ambiente virtual:

.\.venv\Scripts\Activate.ps1

### 5.2. Instalar as dependências

Com o ambiente virtual ativado, execute:

python -m pip install --upgrade pip

pip install -r requirements.txt

### 5.3. Iniciar o Redis

Execute o comando:

docker compose up -d

Para verificar se o container está em execução:

docker ps

Teste a conexão com o Redis:

docker exec redis-celery redis-cli ping

O resultado esperado é:

PONG

## 6. Executando a aplicação

A aplicação utiliza três componentes:

1. Redis: armazena e distribui as mensagens das tarefas.
2. FastAPI: recebe as requisições e envia as tarefas para o Celery.
3. Worker Celery: consome a fila e executa os cálculos.

Cada componente deve ser iniciado em um terminal separado.

### 6.1. Terminal 1 - Redis

Com o Docker Desktop aberto, execute:

docker compose up -d

### 6.2. Terminal 2 - Worker Celery

Ative o ambiente virtual, caso ainda não esteja ativo:

.\.venv\Scripts\Activate.ps1

Inicie o worker:

celery -A celery_app worker -l info --pool=solo

O parâmetro --pool=solo utiliza um processo de execução único,
sendo adequado para testes locais no Windows.

O worker ficará aguardando tarefas enviadas pela API.

### 6.3. Terminal 3 - API FastAPI

Ative o ambiente virtual e execute:

uvicorn main:app --reload

A API estará disponível em:

http://127.0.0.1:8000

A documentação interativa estará disponível em:

http://127.0.0.1:8000/docs

## 7. Testando os endpoints

Os testes podem ser realizados pela documentação Swagger ou
utilizando o PowerShell.

### 7.1. Teste da soma

Envie uma requisição POST para:

http://127.0.0.1:8000/calcular-soma

Corpo JSON:

{
    "a": 10,
    "b": 20
}

Exemplo utilizando PowerShell:

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/calcular-soma" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"a":10,"b":20}'

A API deverá retornar uma resposta semelhante a:

{
    "mensagem": "Tarefa de soma enviada para processamento.",
    "task_id": "identificador-gerado-pelo-celery",
    "status": "pendente"
}

O identificador será gerado automaticamente pelo Celery.

No terminal do worker, após aproximadamente 5 segundos,
será exibido o resultado:

Resultado da soma: 30.0

### 7.2. Teste do fatorial

Envie uma requisição POST para:

http://127.0.0.1:8000/calcular-fatorial

Corpo JSON:

{
    "n": 5
}

Exemplo utilizando PowerShell:

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/calcular-fatorial" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"n":5}'

A resposta da API será semelhante a:

{
    "mensagem": "Tarefa de fatorial enviada para processamento.",
    "task_id": "identificador-gerado-pelo-celery",
    "status": "pendente"
}

Após o processamento, o worker deverá apresentar:

Resultado do fatorial de 5: 120

### 7.3. Teste de validação

O endpoint de fatorial aceita números inteiros entre 0 e 10000.

Uma requisição com número negativo ou superior a 10000
deverá retornar o código HTTP 422 (Unprocessable Entity).

Exemplo de corpo inválido:

{
    "n": -5
}

## 8. Processamento em segundo plano

A integração entre FastAPI, Celery e Redis funciona da seguinte forma:

1. O cliente envia uma requisição para a API.
2. O FastAPI valida os dados recebidos.
3. A tarefa é enviada ao Redis por meio do método .delay().
4. A API retorna o identificador da tarefa e o status pendente.
5. O worker Celery consome a mensagem da fila.
6. O worker executa o cálculo e registra o resultado no log.

O uso de tarefas em segundo plano permite que a API não fique
aguardando a conclusão de operações demoradas.

## 9. Evidências de teste

As evidências devem ser registradas após a execução real
da aplicação.

A pasta evidencias/ deve conter:

- Screenshot da resposta do endpoint de soma.
- Screenshot da resposta do endpoint de fatorial.
- Screenshot ou arquivo de log do worker mostrando os resultados.

Os registros devem demonstrar que as tarefas foram aceitas
pela API e executadas pelo worker.

## 10. Encerramento

Para interromper a API e o worker, pressione Ctrl+C
nos respectivos terminais.

Para interromper o container Redis:

docker compose down

## 11. Conclusão

O projeto demonstra a integração de uma API FastAPI com
Celery e Redis para processamento assíncrono de tarefas.

A atividade permitiu praticar a criação de tarefas, o uso
de filas de mensagens, a execução de workers e a separação
entre recebimento de requisições e processamento em segundo plano.