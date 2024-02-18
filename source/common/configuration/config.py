import pathlib
from urllib import parse

from pydantic import Field
from pydantic_settings import BaseSettings

ROOT_DIRECTORY: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.parent


class DatabaseConfig(BaseSettings):
    DATABASE_NAME: str = Field(default="acetl_database", description="database name")
    DATABASE_USER: str = Field(default="admin", description="db username")
    DATABASE_PASSWORD: str = Field(default="admin", description="DB user password")
    DATABASE_HOST: str = Field(default="localhost", description="Database host")
    DATABASE_PORT: int = Field(default="5442", description="Database Port")

    # should cash this property
    @property
    def database_url(self):
        return (f"postgresql://{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
                f"?user={parse.quote(self.DATABASE_USER)}"
                f"&password={parse.quote(self.DATABASE_PASSWORD)}")
