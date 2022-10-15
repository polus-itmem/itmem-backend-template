from fastapi import Request, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from config import config

from services.web_query import WebQueryController


class SessionMiddleware:
    def __init__(
            self,
            engine,
    ):
        self.engine = engine
        self.session_maker = sessionmaker(engine, expire_on_commit = False, class_ = AsyncSession)

    async def __call__(self, request: Request, call_next):
        if request.headers.get('key') != config.web_secret.get_secret_value():
            return HTTPException(status_code=401, detail="error microservice key")

        async with self.session_maker() as session:
            async with session.begin():
                web_query = WebQueryController(session)
                request.scope['session'] = web_query

                # process the request and get the response
                response: Response = await call_next(request)

                await session.commit()

        await self.engine.dispose()
        return response

