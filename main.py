from contextlib import asynccontextmanager

from fastapi import FastAPI

from source.common.utils.init_db import initialize_database
from source.web_app.apis.csv_api import data_fetch_router
from source.web_app.config.config import AppConfig, app_config
from source.web_app.config.injection import DependencyContainer


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


web_app = FastAPI(lifespan=lifespan)
web_app.container = DependencyContainer()

web_app.include_router(data_fetch_router, tags=["CSV EXTRACTION"])

# Run the FastAPI application with uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:web_app", host=app_config.APP_HOST, port=app_config.APP_PORT,
                workers=app_config.APP_WORKERS_COUNT)
