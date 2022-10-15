import time

import uvicorn
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from starlette.middleware.base import BaseHTTPMiddleware

from config import config
from middlewares import session
from routers import router

app = FastAPI(title = 'Template', version = '1.0.0')


@app.get("/", description = "Server time", response_model = int)
async def time():
    return time.time()


app.add_middleware(BaseHTTPMiddleware,
                   dispatch = session.SessionMiddleware(
                       engine = create_async_engine(config.db.get_secret_value())
                   ))

app.include_router(router)

uvicorn.run(app)
