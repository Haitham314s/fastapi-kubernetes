from celery import Celery
from fastapi import FastAPI

from ecommerce import db
from ecommerce.auth import router as auth_router
from ecommerce.cart import router as cart_router
from ecommerce.config import REDIS_DB, REDIS_HOST, REDIS_PORT
from ecommerce.orders import router as order_router
from ecommerce.products import router as product_router
from ecommerce.user import router as user_router

app = FastAPI(title="Ecommerce App", version="0.0.1")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)

celery = Celery(
    __name__,
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
)

celery.conf.imports = ["ecommerce.orders.tasks"]


@app.on_event("startup")
async def init_db():
    await db.init()


@app.on_event("shutdown")
async def close_db():
    await db.close()
