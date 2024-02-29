from sqlalchemy import create_engine

from source.common.configuration.config import DatabaseConfig

from source.common.models.product_model import Base


def initialize_database():
    db_config = DatabaseConfig()

    engine = create_engine(db_config.database_url)

    Base.metadata.create_all(engine)
