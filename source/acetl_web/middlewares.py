import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# from source.common.configuration.logging_config import logger, context_var_sub
from source.common.configuration.tracing import tracer


class MonitoringMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        span_name = str(uuid.uuid4())

        with tracer.start_as_current_span(span_name) as span:
            start_time = time.time()

            result = await call_next(request)

            end_time = time.time()
            execution_time = end_time - start_time

            span.set_attribute("execution.time", execution_time)
            span.set_attribute("operation.name", span_name)

            return result


from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class TestMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # do something with the request object, for example
        content_type = request.headers.get('Content-Type')
        context_var_sub.set("c56fc41b-d688-4e21-9b07-e0e5733520d5")
        # process the request and get the response
        response = await call_next(request)

        logger.info(f"After request {content_type}")
        return response
