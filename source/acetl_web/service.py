from typing import Type

from source.acetl_web.database_helper import Database
from source.acetl_web.repository import ProductRepository
from source.acetl_web.schema import ProductFirstChunkList
from source.common.configuration.config import DatabaseConfig


class ProductService:
    def __init__(self,
                 product_repository_type: Type[ProductRepository],
                 database_config: DatabaseConfig
                 ):
        self.repository_type: Type[ProductRepository] = product_repository_type
        self.database_config = database_config

    def get_data_overview(self) -> ProductFirstChunkList:
        db_helper = Database(self.database_config.database_url)

        with db_helper.session() as session:
            # using a minimal Unit of Work Pattern
            repository = self.repository_type(session=session)

            return ProductFirstChunkList(data=repository.peek_at_first_chunk())
