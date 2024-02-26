import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

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
