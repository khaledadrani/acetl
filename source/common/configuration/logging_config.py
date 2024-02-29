"""
"timestamp": The date and time when the log entry was created. It is represented in the ISO 8601 format. In this case, the timestamp is "2023-04-18T13:30:00Z".

"level": The severity level of the log entry. Possible values can include ERROR, WARN, INFO, DEBUG, etc. In this example, the level is "INFO".

"message": A brief, human-readable description of the event being logged. Here, the message is "Request received".

"correlation_id": A unique identifier used to correlate log entries across multiple systems or services. In this example, the correlation_id is "1a2b3c4d5e6f".

"session_id": A unique identifier for a user session, often used for tracking user activity. In this case, the session_id is "abcd-1234".

"span_id": A unique identifier for a single unit of work within a distributed trace (openTelemetry), representing the scope of the work being done. Here, the span_id is "9876543210abcdef".

"trace_id": A unique identifier for an end-to-end distributed trace (openTelemetry), allowing individual log entries to be linked together. In this example, the trace_id is "abcdef1234567890".

"service_name": The name of the service or system generating the log entry. In this case, the service_name is "example-service".

"operation_name": The name of the operation or function being executed within the service. Here, the operation_name is "get_user".

"tags": A set of key-value pairs providing additional context and metadata for the log entry. In this example, the tags include "http.method" (GET), "http.path" (/users/123), and "http.status_code" (200).

"log_type": The type of the log entry, such as request, response, or error. In this case, the log_type is "request".

"duration_ms": The duration of the operation or request in milliseconds. In this example, the duration is 50 milliseconds.




{
    "timestamp": "2023-04-18T13:30:00Z",
    "level": "INFO",
    "message": "Request received",
    "correlation_id": "1a2b3c4d5e6f",
    "session_id": "abcd-1234",
    "span_id": "9876543210abcdef",
    "trace_id": "abcdef1234567890",
    "service_name": "example-service",
    "operation_name": "get_user",
    "tags": {
        "http.method": "GET",
        "http.path": "/users/123",
        "http.status_code": 200
    },
    "log_type": "request",
    "duration_ms": 50
}
"""
import contextvars
import json
import logging
import logging.config
import logging.config
from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

context_var_sub = contextvars.ContextVar('sub', default=None)


class Tags(BaseModel):
    http_method: Optional[str] = None
    http_path: Optional[str] = None
    http_status_code: Optional[int] = None


class LogEntry(BaseModel):
    timestamp: Optional[datetime] = None
    level: Optional[str] = None
    message: Optional[str] = None
    correlation_id: Optional[str] = None
    session_id: Optional[str] = None
    span_id: Optional[str] = None
    trace_id: Optional[str] = None
    service_name: Optional[str] = None
    operation_name: Optional[str] = None
    tags: Optional[Tags] = None
    log_type: Optional[str] = None
    duration_ms: Optional[int] = None


class StandardLogRecordHandler(logging.StreamHandler):
    """Handler for a streaming logging request.

    This basically logs the record using whatever logging policy is
    configured locally.
    """

    # def emit(self, record):
    #     # if a name is specified, we use the named logger rather than the one
    #     # implied by the record.
    #     # print(record)
    #
    #     # N.B. EVERY record gets logged. This is because Logger.handle
    #     # is normally called AFTER logger-level filtering. If you want
    #     # to do filtering, do it at the client end to save wasting
    #     # cycles and network bandwidth!
    #     user_id = context_var_sub.get()
    #
    #     # print("user id ", user_id)
    #     # print("hey you")
    #     return record

    # this will overide formatter
    def format_log_entry(self, record) -> str:
        tags = Tags()
        tags.http_method = "GET"  # Filling with default values
        tags.http_path = "/default/path"
        tags.http_status_code = 200

        log_entry = LogEntry(
            timestamp=datetime.fromtimestamp(record.created),
            level=record.levelname,
            message=record.getMessage(),
            service_name=record.module,
            operation_name=record.funcName,
            tags=tags,
            log_type="request",
            duration_ms=1000  # Example duration
        )
        return json.dumps(jsonable_encoder(log_entry.model_dump()))

    def format(self, record):
        formatted_record = self.format_log_entry(record)
        return formatted_record


def create_logger(name: str = __name__, logging_level: int = logging.INFO) -> logging.Logger:
    # try this later logging.config.fileConfig('logging.conf')
    logger = logging.getLogger(name)
    logger.setLevel(logging_level)

    # create console handler and set level to debug
    stream_handler = StandardLogRecordHandler()  # logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(lineno)d - %(funcName)s - %(levelname)s - %(message)s')
    # add formatter to ch
    stream_handler.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(stream_handler)

    return logger


# if False:
#     # make sure that you import this logger
#     logging.config.fileConfig(fname='log_config.ini', disable_existing_loggers=False)
#     logger = logging.getLogger(__name__)
#
# else:
logger = create_logger()
