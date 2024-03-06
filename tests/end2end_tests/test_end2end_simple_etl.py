import pathlib

from sqlalchemy import create_engine

from source.etl_acetl.simple_etl import SimpleETLPipeline
from source.common.configuration.config import DatabaseConfig
from source.common.models.product_model import Base


def simple_etl_testing(data_path: str):
    """
    TODO, not exactly a test, need to be completed
    :param data_path:
    :return:
    """
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
