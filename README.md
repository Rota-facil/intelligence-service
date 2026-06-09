# intelligence-service

Servico de inteligencia do Rota Facil. E uma API FastAPI em Python que registra sua instancia no Eureka, gera interpretacoes operacionais de rotas usando OpenAI e cria mapas de calor de pontos de embarque usando Plotly.

## Para que serve

- Interpretar historico de viagens finalizadas de uma rota e produzir um resumo operacional objetivo.
- Identificar atrasos, cancelamentos, pontualidade, padroes recorrentes e tendencias a partir dos dados enviados pelo `transport-service`.
- Gerar imagem PNG de mapa de calor dos pontos de embarque mais usados em viagens finalizadas.
- Enviar o mapa de calor gerado para o `file-service` e devolver a URL pre-assinada do arquivo.

## Stack

- Python 3.12.
- FastAPI e Uvicorn.
- Pydantic para DTOs.
- `py_eureka_client` para registro no Eureka.
- OpenAI SDK, modelo `gpt-4.1-nano`.
- Pandas e Plotly Express para montar o mapa de densidade.
- Kaleido/Chromium para exportar o grafico como PNG.
- Requests para enviar o arquivo ao `file-service`.

## Estrutura

- `main.py`: inicializa FastAPI, registra no Eureka durante o lifespan e inclui o router de inteligencia.
- `http_routes/controllers/intelligence_controller.py`: declara endpoints `/intelligence`.
- `http_routes/dto/`: modelos Pydantic de entrada.
- `business/open_ai_service.py`: monta o prompt e chama a OpenAI.
- `business/heat_maps_service.py`: gera mapa de calor, exporta PNG e faz upload no `file-service`.
- `requirements.txt`: dependencias Python.
- `Dockerfile`: imagem Python 3.12 slim com Chromium/Kaleido.

## Porta e descoberta

- Porta: `8000`.
- App Eureka: `intelligence-service`.
- Host default: `localhost`.
- Eureka default: `http://localhost:8081/eureka/`.

No compose geral do Rota Facil, o servico usa:

- `INTELLIGENCE_SERVICE_BASE_URL=http://intelligence-service:8000`
- `INTELLIGENCE_HOST=intelligence-service`
- `EUREKA_SERVER=http://eureka-service:8081/eureka`

## Endpoints

### `GET /`

Endpoint simples de raiz.

Resposta:

```json
{ "message": "Hello World" }
```

### `GET /hello/{name}`

Endpoint simples de teste.

Resposta:

```json
{ "message": "Hello User" }
```

### `GET /intelligence/`

Health check funcional do modulo de inteligencia.

Resposta:

```json
"intelligence-service is running"
```

### `POST /intelligence/route/interpretation`

Recebe dados historicos de uma rota e retorna uma interpretacao textual.

Request:

```json
{
  "expectedGoing": "07:00:00",
  "expectedGoingFinish": "08:00:00",
  "expectedReturn": "17:00:00",
  "expectedReturnFinish": "18:00:00",
  "shift": "MORNING",
  "recurringDays": ["MONDAY", "WEDNESDAY"],
  "tripHistory": [
    {
      "expectedInstitutionsPassed": ["Escola A", "Escola B"],
      "actualInstitutionsPassed": ["Escola A"],
      "status": [
        {
          "progress": "FINISHED",
          "delay": "ON_TIME",
          "eventOccurred": "2026-06-08T07:30:00"
        }
      ]
    }
  ]
}
```

Response:

```json
{
  "routeInterpretation": "Texto objetivo com insights operacionais da rota."
}
```

A implementacao instrui o modelo a responder em ate 2 paragrafos, com metricas proporcionais/percentuais quando possivel, sem inventar dados.

### `POST /intelligence/route/heat-map`

Recebe pontos geograficos de embarque, gera um mapa de densidade em PNG, envia o arquivo para o `file-service` e retorna a URL pre-assinada recebida.

Request:

```json
{
  "currentUser": {
    "userId": "00000000-0000-0000-0000-000000000000",
    "prefectureId": "00000000-0000-0000-0000-000000000000",
    "email": "admin@exemplo.com",
    "role": "ADMIN"
  },
  "routeId": "00000000-0000-0000-0000-000000000000",
  "points": [
    { "latitude": -3.7319, "longitude": -38.5267 },
    { "latitude": -3.7321, "longitude": -38.5270 }
  ]
}
```

Response:

```json
{
  "preSignedUrlHeatMap": "https://..."
}
```

## Integracao com file-service

Para mapa de calor, o servico chama:

```text
POST {BASE_FILE_SERVICE_URL}/heat-map/{routeId}
```

Default local:

```text
BASE_FILE_SERVICE_URL=http://localhost:8088/files
```

O upload e feito como multipart com campo `file`, nome `heatmap.png` e content type `image/png`.

Headers propagados para o `file-service`:

- `x-user-id`
- `x-user-email`
- `x-user-role`
- `x-prefecture-id`

## Variaveis de ambiente

- `OPEN_AI_API_KEY`: chave usada pelo SDK da OpenAI.
- `EUREKA_SERVER`: URL do Eureka. Default `http://localhost:8081/eureka/`.
- `INTELLIGENCE_HOST`: host registrado no Eureka. Default `localhost`.
- `BASE_FILE_SERVICE_URL`: URL base do `file-service`. Default `http://localhost:8088/files`.

## Como rodar localmente

Crie e ative um ambiente virtual:

```bash
cd /home/tagashi/PycharmProjects/intelligence-service
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configure variaveis necessarias:

```bash
export OPEN_AI_API_KEY=...
export EUREKA_SERVER=http://localhost:8081/eureka/
export BASE_FILE_SERVICE_URL=http://localhost:8088/files
```

Rode a API:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

A aplicacao tenta se registrar no Eureka no startup e fica tentando novamente a cada 5 segundos enquanto o Eureka nao estiver pronto.

## Como rodar com Docker

Build:

```bash
docker build -t rota-facil-intelligence-service .
```

Run:

```bash
docker run --rm -p 8000:8000 \
  -e OPEN_AI_API_KEY=... \
  -e EUREKA_SERVER=http://host.docker.internal:8081/eureka/ \
  -e INTELLIGENCE_HOST=localhost \
  -e BASE_FILE_SERVICE_URL=http://host.docker.internal:8088/files \
  rota-facil-intelligence-service
```

No compose geral do projeto, a imagem usada e `thaua1/rota-facil-intelligence-service`.

## Como testar rapidamente

Com a API rodando:

```bash
curl http://localhost:8000/intelligence/
```

Para testar interpretacao ou heat map, use payloads compatíveis com os DTOs acima. O mapa de calor depende do `file-service` acessivel e autenticacao por headers propagados.

## Especializacao

Este servico concentra analise inteligente e geracao de artefatos analiticos. Ele nao deve manter regras transacionais de rotas, viagens, usuarios ou arquivos; essas responsabilidades continuam em `transport-service`, `auth-service` e `file-service`.
