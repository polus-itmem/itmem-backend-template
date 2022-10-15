import time

import uvicorn
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from starlette.middleware.base import BaseHTTPMiddleware

from config import config
from middlewares import session
from models import Time
from routers import router

app = FastAPI(title = 'Template')


@app.get("/", description = "Server time", response_model = Time)
async def root() -> Time:
    return Time(time = time.time())


app.add_middleware(BaseHTTPMiddleware,
                   dispatch = session.SessionMiddleware(
                       engine = create_async_engine(config.db.get_secret_value())
                   ))

app.include_router(router)

uvicorn.run(app)
