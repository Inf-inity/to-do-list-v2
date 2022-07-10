from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from database import db_context


class HTTPMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)

    @staticmethod
    async def set_body(request: Request):
        receive_ = await request._receive()

        async def receive():
            return receive_

        request._receive = receive

    async def dispatch(self, request, call_next):
        await self.set_body(request)

        async with db_context():
            return await call_next(request)
