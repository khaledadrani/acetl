import pathlib

from sqlalchemy import create_engine

from source.configuration.config import DatabaseConfig
from source.core.simple_etl import SimpleETLPipeline
from source.models.product_model import Base


def test_simple_etl(data_path: str):
    engine = create_engine(DatabaseConfig().database_url)

    Base.metadata.create_all(engine)

    db_url = DatabaseConfig().database_url

    data_path = pathlib.Path(data_path)

    if not data_path.exists():
        raise Exception(f"Does not exist! {data_path.absolute()}")

    etl = SimpleETLPipeline(data_path=data_path, database_url=db_url)

    etl.extract()

    etl.transform()

    etl.load()