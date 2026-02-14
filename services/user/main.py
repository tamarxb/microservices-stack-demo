from fastapi import FastAPI, Request
import logging
from prometheus_client import Counter, start_http_server

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("user-service")

# Prometheus metrics
USERS_COUNTER = Counter('users_requests_total', 'Number of /users requests')
start_http_server(8003)  # port for metrics

app = FastAPI()

@app.get("/health")
def health():
    logger.info("Health check called")
    return {"status": "ok"}

@app.get("/users")
def get_users(request: Request):
    logger.info("GET /users called")
    USERS_COUNTER.inc()  # update metrics
    return [{"id": 1, "name": "Tamar"}]
