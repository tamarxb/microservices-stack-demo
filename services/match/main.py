from fastapi import FastAPI, Request
import redis
import logging
from prometheus_client import Counter, start_http_server

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("match-service")

# Prometheus metrics
MATCH_COUNTER = Counter('matches_created_total', 'Number of matches created')
start_http_server(8003)  # port to metrics

app = FastAPI()

r = redis.Redis(host="redis", port=6379, decode_responses=True)

@app.get("/health")
def health():
    logger.info("Health check called")
    return {"status": "ok"}

@app.post("/match/{user_id}")
def match(user_id: int, request: Request):
    logger.info(f"POST /match/{user_id} called")
    r.set(f"match:{user_id}", "true")
    MATCH_COUNTER.inc()  # updating metric
    return {"matched": True}
