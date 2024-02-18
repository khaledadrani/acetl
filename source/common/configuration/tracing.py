import time
from typing import Callable, Any

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("acetl.tracer")


def trace_process(func: Callable, span_name: str, *args, **kwargs) -> Any:
    """
    TODO implement a more robust way of tracing
    TODO a logging solution such as Fluentd or Loki to collect logs from all components
    :param func:
    :param span_name:
    :param args:
    :param kwargs:
    :return:
    """
    with tracer.start_as_current_span(span_name) as span:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time

        span.set_attribute("execution.time", execution_time)
        span.set_attribute("operation.name", span_name)

        return result
