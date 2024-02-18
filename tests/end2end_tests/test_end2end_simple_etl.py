import pathlib

from sqlalchemy import create_engine

from source.common.configuration import DatabaseConfig
from source.acetl_etl.simple_etl import SimpleETLPipeline
from source.common.models import Base


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