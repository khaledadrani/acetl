from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from source.acetl_web.apis import data_fetch_router
from source.acetl_web.app_config import AppConfig
from source.acetl_web.inversion_of_control import DependencyContainer
from source.acetl_web.middlewares import MonitoringMiddleware
from source.common.configuration.logging_config import logger
from source.common.utils.init_db import initialize_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    logger.warning("Initialized DB success!")
    yield


web_app = FastAPI(lifespan=lifespan)
web_app.container = DependencyContainer()

# web_app.add_middleware(MonitoringMiddleware)

app_config = AppConfig()

web_app.include_router(data_fetch_router, tags=["LLM GENERATION API"])
Instrumentator().instrument(web_app).expose(web_app)

# Run the FastAPI application with uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:web_app", host=app_config.APP_HOST, port=app_config.APP_PORT,
                workers=app_config.APP_WORKERS_COUNT)
