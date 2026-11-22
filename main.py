import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from core.handlers import ExcepcionesGlobales
from modules.productos.router import router as router_productos


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("API")

app = FastAPI(title="Sistema de Almacen", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ExcepcionesGlobales.registrar_handlers(app)
app.include_router(router_productos)


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


@app.middleware("http")
async def medir_tiempo(request: Request, call_next):
    inicio = time.perf_counter()
    response = await call_next(request)
    tiempo = (time.perf_counter() - inicio) * 1000
    response.headers["X-Process-Time-Ms"] = f"{tiempo:.2f}"
    logger.info(
        "%s %s | %s | %.2fms",
        request.method,
        request.url.path,
        response.status_code,
        tiempo,
    )
    return response
