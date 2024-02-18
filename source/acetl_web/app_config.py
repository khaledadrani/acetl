from pydantic import Field
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    APP_HOST: str = Field(default="localhost")
    APP_PORT: int = Field(default=8000)
    PROJECT_NAME: str = Field(default="Langroid")
    ROOT_PATH: str = Field(default="/api")
    API_VERSION: str = Field(default='/v1')
    APP_WORKERS_COUNT: int = Field(default=1)

    DEBUG: bool = Field(description="Use this to enable dev and debugging features", default=False)

