from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.middlewares.auth_middleware import unified_auth_middleware
from app.api.routers import order_router
from app.core.db import check_connection
from app.core.logger_config import logger
from app.models.order_items import OrderItem  # noqa: F401
from app.models.orders import Order  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск приложения...")

    await check_connection()

    yield
    logger.info("Остановка приложения...")


app = FastAPI(lifespan=lifespan, title="Maxberries Order Service")


Instrumentator().instrument(app).expose(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(unified_auth_middleware)


app.include_router(order_router)


@app.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok"}
